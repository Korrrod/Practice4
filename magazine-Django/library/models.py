from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название категории")
    description = models.TextField(blank=True, verbose_name="Описание")
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=200, verbose_name="Имя автора")
    bio = models.TextField(blank=True, verbose_name="Биография")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    
    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Book(models.Model):
    STATUS_CHOICES = [
        ('available', 'Доступна'),
        ('rented', 'В аренде'),
        ('sold', 'Продана'),
        ('unavailable', 'Недоступна'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Название")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books', verbose_name="Автор")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='books', verbose_name="Категория")
    year = models.IntegerField(verbose_name="Год написания")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена покупки")
    rental_price_2weeks = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Цена аренды (2 недели)")
    rental_price_1month = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Цена аренды (1 месяц)")
    rental_price_3months = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Цена аренды (3 месяца)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available', verbose_name="Статус")
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True, verbose_name="Обложка")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.author.name}"
    
    def is_available(self):
        return self.status == 'available'

    def current_renter(self):
        rental = self.rentals.filter(is_active=True).first()
        return rental.user if rental else None


class Rental(models.Model):
    PERIOD_CHOICES = [
        ('2weeks', '2 недели'),
        ('1month', '1 месяц'),
        ('3months', '3 месяца'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rentals', verbose_name="Пользователь")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='rentals', verbose_name="Книга")
    period = models.CharField(max_length=20, choices=PERIOD_CHOICES, verbose_name="Период аренды")
    start_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата начала")
    end_date = models.DateTimeField(verbose_name="Дата окончания")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена аренды")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    reminder_sent = models.BooleanField(default=False, verbose_name="Напоминание отправлено")
    
    class Meta:
        verbose_name = "Аренда"
        verbose_name_plural = "Аренды"
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.period})"
    
    def save(self, *args, **kwargs):
        if not self.end_date:
            period_days = {
                '2weeks': 14,
                '1month': 30,
                '3months': 90,
            }
            self.end_date = timezone.now() + timedelta(days=period_days.get(self.period, 14))
        super().save(*args, **kwargs)
    
    def is_expired(self):
        return timezone.now() > self.end_date
    
    def days_remaining(self):
        if self.is_expired():
            return 0
        return (self.end_date - timezone.now()).days


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases', verbose_name="Пользователь")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='purchases', verbose_name="Книга")
    purchase_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата покупки")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена покупки")
    
    class Meta:
        verbose_name = "Покупка"
        verbose_name_plural = "Покупки"
        ordering = ['-purchase_date']
    
    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
