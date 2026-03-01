from django.contrib import admin
from .models import Book, Category, Author, Rental, Purchase


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'birth_date']
    search_fields = ['name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'year', 'status', 'price']
    list_filter = ['status', 'category', 'author', 'year']
    search_fields = ['title', 'author__name']
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'author', 'category', 'year', 'description', 'cover_image')
        }),
        ('Цены', {
            'fields': ('price', 'rental_price_2weeks', 'rental_price_1month', 'rental_price_3months')
        }),
        ('Статус', {
            'fields': ('status',)
        }),
    )


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'period', 'start_date', 'end_date', 'is_active', 'reminder_sent']
    list_filter = ['is_active', 'period', 'reminder_sent']
    search_fields = ['user__username', 'book__title']
    readonly_fields = ['start_date']
    
    def delete_model(self, request, obj):
        """При удалении аренды возвращаем книгу в доступное состояние"""
        book = obj.book
        super().delete_model(request, obj)
        # Проверяем, нет ли других активных аренд этой книги
        if not Rental.objects.filter(book=book, is_active=True).exists():
            book.status = 'available'
            book.save()
    
    def delete_queryset(self, request, queryset):
        """При массовом удалении аренд обновляем статусы книг"""
        books_to_update = set()
        for rental in queryset:
            books_to_update.add(rental.book)
        
        super().delete_queryset(request, queryset)
        
        # Обновляем статусы книг, если нет других активных аренд
        for book in books_to_update:
            if not Rental.objects.filter(book=book, is_active=True).exists():
                book.status = 'available'
                book.save()


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'purchase_date', 'price']
    list_filter = ['purchase_date']
    search_fields = ['user__username', 'book__title']
    readonly_fields = ['purchase_date']
    
    def delete_model(self, request, obj):
        """При удалении покупки возвращаем книгу в доступное состояние"""
        book = obj.book
        super().delete_model(request, obj)
        # Проверяем, нет ли других покупок этой книги
        if not Purchase.objects.filter(book=book).exists():
            book.status = 'available'
            book.save()
    
    def delete_queryset(self, request, queryset):
        """При массовом удалении покупок обновляем статусы книг"""
        books_to_update = set()
        for purchase in queryset:
            books_to_update.add(purchase.book)
        
        super().delete_queryset(request, queryset)
        
        # Обновляем статусы книг, если нет других покупок
        for book in books_to_update:
            if not Purchase.objects.filter(book=book).exists():
                book.status = 'available'
                book.save()
