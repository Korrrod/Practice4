from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg, F
from .models import Travel
from .forms import TravelForm


def home(request):
    search_query = request.GET.get('search', '')
    region = request.GET.get('region', '')
    year = request.GET.get('year', '')
    sort = request.GET.get('sort', 'newest')

    travels = Travel.objects.annotate(
        avg_rating=(F('transport_rating') + F('safety_rating') +
                    F('population_rating') + F('vegetation_rating'))
    )

    if search_query:
        travels = travels.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    if region:
        travels = travels.filter(location__icontains=region)
    if year:
        travels = travels.filter(created_at__year=year)

    if sort == 'rating_high':
        travels = travels.order_by('-avg_rating')
    elif sort == 'rating_low':
        travels = travels.order_by('avg_rating')
    elif sort == 'oldest':
        travels = travels.order_by('created_at')
    elif sort == 'price_high':
        travels = travels.order_by('-cost')
    elif sort == 'price_low':
        travels = travels.order_by('cost')
    else:
        travels = travels.order_by('-created_at')

    years = Travel.objects.dates('created_at', 'year', order='DESC')

    return render(request, 'travels/home.html', {
        'travels': travels,
        'search_query': search_query,
        'region': region,
        'year': year,
        'sort': sort,
        'years': years,
    })


def travel_list(request):
    return redirect('home')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт создан для {username}!')
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'travels/register.html', {'form': form})


def travel_detail(request, pk):
    travel = get_object_or_404(Travel, pk=pk)
    ratings = [
        ('Удобство передвижения', travel.transport_rating),
        ('Безопасность',          travel.safety_rating),
        ('Населенность',          travel.population_rating),
        ('Растительность',        travel.vegetation_rating),
    ]
    return render(request, 'travels/travel_detail.html', {'travel': travel, 'ratings': ratings})


@login_required
def travel_create(request):
    if request.method == 'POST':
        form = TravelForm(request.POST, request.FILES)
        if form.is_valid():
            travel = form.save(commit=False)
            travel.user = request.user
            travel.save()
            messages.success(request, 'Путешествие успешно создано!')
            return redirect('travel_detail', pk=travel.pk)
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = TravelForm()
    return render(request, 'travels/travel_form.html', {'form': form, 'title': 'Создать путешествие'})


@login_required
def travel_edit(request, pk):
    travel = get_object_or_404(Travel, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TravelForm(request.POST, request.FILES, instance=travel)
        if form.is_valid():
            form.save()
            messages.success(request, 'Путешествие обновлено!')
            return redirect('travel_detail', pk=travel.pk)
    else:
        form = TravelForm(instance=travel)
    return render(request, 'travels/travel_form.html', {'form': form, 'title': 'Редактировать путешествие'})


@login_required
def my_travels(request):
    travels = Travel.objects.filter(user=request.user)
    return render(request, 'travels/my_travels.html', {'travels': travels})
