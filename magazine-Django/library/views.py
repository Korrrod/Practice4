from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.http import JsonResponse
from .models import Book, Category, Author, Rental, Purchase
from datetime import timedelta


def is_admin(user):
    return user.is_authenticated and user.is_staff


def register_view(request):
    if request.user.is_authenticated:
        return redirect('book_list')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        
        # Валидация
        errors = []
        
        if not username:
            errors.append('Имя пользователя обязательно.')
        elif User.objects.filter(username=username).exists():
            errors.append('Пользователь с таким именем уже существует.')
        
        if not email:
            errors.append('Email обязателен.')
        elif User.objects.filter(email=email).exists():
            errors.append('Пользователь с таким email уже существует.')
        
        if not password1:
            errors.append('Пароль обязателен.')
        elif len(password1) < 8:
            errors.append('Пароль должен содержать минимум 8 символов.')
        
        if password1 != password2:
            errors.append('Пароли не совпадают.')
        
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password1,
                    first_name=first_name,
                    last_name=last_name
                )
                messages.success(request, 'Регистрация успешна! Теперь вы можете войти.')
                return redirect('login')
            except Exception as e:
                messages.error(request, f'Ошибка при регистрации: {str(e)}')
    
    return render(request, 'library/register.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('book_list')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {user.username}!')
                next_url = request.GET.get('next', 'book_list')
                return redirect(next_url)
            else:
                messages.error(request, 'Неверное имя пользователя или пароль.')
        else:
            messages.error(request, 'Пожалуйста, заполните все поля.')
    
    return render(request, 'library/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('book_list')


def search_suggestions(request):
    query = request.GET.get('q', '').strip()
    results = []
    if len(query) >= 1:
        books = Book.objects.filter(
            Q(title__icontains=query) | Q(author__name__icontains=query)
        ).select_related('author')[:8]
        for book in books:
            results.append({'label': f'{book.title} | {book.author.name}', 'value': book.title})
    return JsonResponse(results, safe=False)


def book_list(request):
    books = Book.objects.all()
    categories = Category.objects.all()
    authors = Author.objects.all()
    
    # Фильтрация
    category_filter = request.GET.get('category')
    author_filter = request.GET.get('author')
    year_filter = request.GET.get('year')
    search_query = request.GET.get('search', '')
    
    if category_filter:
        books = books.filter(category_id=category_filter)
    if author_filter:
        books = books.filter(author_id=author_filter)
    if year_filter:
        books = books.filter(year=year_filter)
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Сортировка
    sort_by = request.GET.get('sort', 'title')
    if sort_by == 'category':
        books = books.order_by('category__name', 'title').distinct()
    elif sort_by == 'author':
        books = books.order_by('author__name', 'title')
    elif sort_by == 'year':
        books = books.order_by('-year', 'title')
    else:
        books = books.order_by('title')
    
    # Получаем уникальные годы для фильтра
    years = Book.objects.values_list('year', flat=True).distinct().order_by('-year')
    
    # Баннер истекающих аренд для авторизованного пользователя
    expiring_rentals = []
    if request.user.is_authenticated and not request.user.is_staff:
        now = timezone.now()
        soon = now + timedelta(days=3)
        active = Rental.objects.filter(
            user=request.user,
            is_active=True,
            end_date__gte=now,
            end_date__lte=soon,
        ).select_related('book')
        for rental in active:
            delta = (rental.end_date.date() - now.date()).days
            expiring_rentals.append({'rental': rental, 'days_left': delta})

    context = {
        'books': books,
        'categories': categories,
        'authors': authors,
        'years': years,
        'current_category': category_filter,
        'current_author': author_filter,
        'current_year': year_filter,
        'current_sort': sort_by,
        'search_query': search_query,
        'expiring_rentals': expiring_rentals,
    }
    return render(request, 'library/book_list.html', context)


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    context = {
        'book': book,
    }
    return render(request, 'library/book_detail.html', context)


@login_required
def rent_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        period = request.POST.get('period')
        
        if not period:
            messages.error(request, 'Не выбран период аренды.')
            return redirect('book_detail', pk=pk)
        
        if not book.is_available():
            messages.error(request, 'Эта книга недоступна для аренды.')
            return redirect('book_detail', pk=pk)
        
        # Проверяем, не арендована ли уже эта книга пользователем
        active_rental = Rental.objects.filter(user=request.user, book=book, is_active=True).first()
        if active_rental:
            messages.warning(request, 'Вы уже арендовали эту книгу.')
            return redirect('book_detail', pk=pk)
        
        # Определяем цену в зависимости от периода
        price_map = {
            '2weeks': book.rental_price_2weeks,
            '1month': book.rental_price_1month,
            '3months': book.rental_price_3months,
        }
        price = price_map.get(period, 0)
        
        if price <= 0:
            messages.error(request, 'Цена аренды не установлена для выбранного периода.')
            return redirect('book_detail', pk=pk)
        
        try:
            # Создаем аренду
            rental = Rental.objects.create(
                user=request.user,
                book=book,
                period=period,
                price=price
            )
            
            # Обновляем статус книги
            book.status = 'rented'
            book.save()
            
            messages.success(request, f'Книга успешно арендована до {rental.end_date.strftime("%d.%m.%Y")}.')
            return redirect('my_rentals')
        except Exception as e:
            messages.error(request, f'Ошибка при создании аренды: {str(e)}')
            return redirect('book_detail', pk=pk)
    
    return redirect('book_detail', pk=pk)


@login_required
def purchase_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        if book.status == 'sold':
            messages.error(request, 'Эта книга уже продана.')
            return redirect('book_detail', pk=pk)
        
        if not book.is_available():
            messages.error(request, 'Эта книга недоступна для покупки.')
            return redirect('book_detail', pk=pk)
        
        try:
            # Создаем покупку
            purchase = Purchase.objects.create(
                user=request.user,
                book=book,
                price=book.price
            )
            
            # Обновляем статус книги
            book.status = 'sold'
            book.save()
            
            messages.success(request, 'Книга успешно куплена!')
            return redirect('my_purchases')
        except Exception as e:
            messages.error(request, f'Ошибка при покупке книги: {str(e)}')
            return redirect('book_detail', pk=pk)
    
    return redirect('book_detail', pk=pk)


@login_required
def my_rentals(request):
    rentals = Rental.objects.filter(user=request.user).order_by('-start_date')
    context = {
        'rentals': rentals,
    }
    return render(request, 'library/my_rentals.html', context)


@login_required
def my_purchases(request):
    purchases = Purchase.objects.filter(user=request.user).order_by('-purchase_date')
    context = {
        'purchases': purchases,
    }
    return render(request, 'library/my_purchases.html', context)


@user_passes_test(is_admin)
def admin_users(request):
    search = request.GET.get('search', '')
    users = User.objects.filter(is_staff=False)
    if search:
        users = users.filter(Q(username__icontains=search) | Q(first_name__icontains=search))
    users = users.order_by('username')
    return render(request, 'library/admin_users.html', {'users': users, 'search': search})


@user_passes_test(is_admin)
def admin_user_detail(request, pk):
    target = get_object_or_404(User, pk=pk)
    rentals = Rental.objects.filter(user=target).order_by('-start_date')
    purchases = Purchase.objects.filter(user=target).order_by('-purchase_date')
    return render(request, 'library/admin_user_detail.html', {
        'target': target,
        'rentals': rentals,
        'purchases': purchases,
    })


@user_passes_test(is_admin)
def admin_dashboard(request):
    total_books = Book.objects.count()
    total_rentals = Rental.objects.filter(is_active=True).count()
    total_purchases = Purchase.objects.count()
    expired_rentals = Rental.objects.filter(is_active=True, end_date__lt=timezone.now())
    expiring_soon = Rental.objects.filter(
        is_active=True,
        end_date__gte=timezone.now(),
        end_date__lte=timezone.now() + timedelta(days=3)
    )
    
    context = {
        'total_books': total_books,
        'total_rentals': total_rentals,
        'total_purchases': total_purchases,
        'expired_rentals': expired_rentals,
        'expiring_soon': expiring_soon,
    }
    return render(request, 'library/admin_dashboard.html', context)


@user_passes_test(is_admin)
def admin_books(request):
    books = Book.objects.all().order_by('-created_at')
    
    # Фильтрация
    status_filter = request.GET.get('status')
    if status_filter:
        books = books.filter(status=status_filter)
    
    context = {
        'books': books,
        'status_choices': Book.STATUS_CHOICES,
        'current_status': status_filter,
    }
    return render(request, 'library/admin_books.html', context)


@user_passes_test(is_admin)
def admin_book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        try:
            book.title = request.POST.get('title')
            book.author_id = request.POST.get('author')
            category_id = request.POST.get('category')
            book.category_id = int(category_id) if category_id else None
            book.year = int(request.POST.get('year'))
            book.description = request.POST.get('description', '')
            book.price = float(request.POST.get('price', 0))
            book.rental_price_2weeks = float(request.POST.get('rental_price_2weeks') or 0)
            book.rental_price_1month = float(request.POST.get('rental_price_1month') or 0)
            book.rental_price_3months = float(request.POST.get('rental_price_3months') or 0)
            book.status = request.POST.get('status', 'available')
            book.save()
            
            messages.success(request, 'Книга успешно обновлена.')
            return redirect('admin_books')
        except (ValueError, TypeError) as e:
            messages.error(request, f'Ошибка при обновлении книги: {str(e)}')
            return redirect('admin_book_edit', pk=pk)
    
    categories = Category.objects.all()
    authors = Author.objects.all()
    context = {
        'book': book,
        'categories': categories,
        'authors': authors,
        'status_choices': Book.STATUS_CHOICES,
    }
    return render(request, 'library/admin_book_edit.html', context)


@user_passes_test(is_admin)
def admin_book_add(request):
    if request.method == 'POST':
        try:
            category_id = request.POST.get('category')
            book = Book.objects.create(
                title=request.POST.get('title'),
                author_id=int(request.POST.get('author')),
                category_id=int(category_id) if category_id else None,
                year=int(request.POST.get('year')),
                description=request.POST.get('description', ''),
                price=float(request.POST.get('price', 0)),
                rental_price_2weeks=float(request.POST.get('rental_price_2weeks') or 0),
                rental_price_1month=float(request.POST.get('rental_price_1month') or 0),
                rental_price_3months=float(request.POST.get('rental_price_3months') or 0),
                status=request.POST.get('status', 'available'),
            )
            messages.success(request, 'Книга успешно добавлена.')
            return redirect('admin_books')
        except (ValueError, TypeError) as e:
            messages.error(request, f'Ошибка при добавлении книги: {str(e)}. Проверьте правильность введенных данных.')
            return redirect('admin_book_add')
    
    categories = Category.objects.all()
    authors = Author.objects.all()
    context = {
        'categories': categories,
        'authors': authors,
        'status_choices': Book.STATUS_CHOICES,
    }
    return render(request, 'library/admin_book_add.html', context)


@user_passes_test(is_admin)
def admin_book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        # Проверяем, нет ли активных аренд этой книги
        active_rentals = Rental.objects.filter(book=book, is_active=True).exists()
        if active_rentals:
            messages.error(request, 'Нельзя удалить книгу, которая находится в активной аренде.')
            return redirect('admin_books')
        
        book.delete()
        messages.success(request, 'Книга успешно удалена.')
        return redirect('admin_books')
    
    # Проверяем наличие активных аренд
    active_rentals = Rental.objects.filter(book=book, is_active=True)
    context = {
        'book': book,
        'active_rentals': active_rentals,
    }
    return render(request, 'library/admin_book_delete.html', context)


@user_passes_test(is_admin)
def admin_rentals(request):
    rentals = Rental.objects.all().order_by('-start_date')
    
    # Фильтрация
    status_filter = request.GET.get('status')
    if status_filter == 'expired':
        rentals = rentals.filter(is_active=True, end_date__lt=timezone.now())
    elif status_filter == 'active':
        rentals = rentals.filter(is_active=True, end_date__gte=timezone.now())
    elif status_filter == 'inactive':
        rentals = rentals.filter(is_active=False)
    
    context = {
        'rentals': rentals,
    }
    return render(request, 'library/admin_rentals.html', context)


@user_passes_test(is_admin)
def admin_rental_delete(request, pk):
    rental = get_object_or_404(Rental, pk=pk)
    book = rental.book
    
    if request.method == 'POST':
        rental.delete()
        # Проверяем, нет ли других активных аренд этой книги
        if not Rental.objects.filter(book=book, is_active=True).exists():
            book.status = 'available'
            book.save()
        messages.success(request, 'Аренда успешно удалена.')
        return redirect('admin_rentals')
    
    context = {
        'rental': rental,
    }
    return render(request, 'library/admin_rental_delete.html', context)


@user_passes_test(is_admin)
def admin_purchases(request):
    purchases = Purchase.objects.all().order_by('-purchase_date')
    
    context = {
        'purchases': purchases,
    }
    return render(request, 'library/admin_purchases.html', context)


@user_passes_test(is_admin)
def admin_purchase_delete(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)
    book = purchase.book
    
    if request.method == 'POST':
        purchase.delete()
        # Проверяем, нет ли других покупок этой книги
        if not Purchase.objects.filter(book=book).exists():
            book.status = 'available'
            book.save()
        messages.success(request, 'Покупка успешно удалена. Книга возвращена в каталог.')
        return redirect('admin_purchases')
    
    context = {
        'purchase': purchase,
    }
    return render(request, 'library/admin_purchase_delete.html', context)
