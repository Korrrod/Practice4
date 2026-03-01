from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Travel(models.Model):
    """Модель путешествия"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='travels', verbose_name='Пользователь')
    title = models.CharField(max_length=200, verbose_name='Название путешествия')
    description = models.TextField(verbose_name='Описание')
    location = models.CharField(max_length=200, verbose_name='Местоположение')
    
    # Изображение мест
    image = models.ImageField(upload_to='travel_images/', blank=True, null=True, verbose_name='Изображение')
    
    # Стоимость путешествия
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость путешествия', 
                               help_text='Стоимость в рублях')
    
    # Места для посещения
    places_to_visit = models.TextField(verbose_name='Места для посещения', 
                                       help_text='Перечислите места через запятую или каждое с новой строки')
    
    # Оценки (от 1 до 10)
    transport_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Оценка удобства передвижения',
        help_text='Оценка от 1 до 10'
    )
    safety_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Оценка безопасности',
        help_text='Оценка от 1 до 10'
    )
    population_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Оценка населенности',
        help_text='Оценка от 1 до 10'
    )
    vegetation_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Оценка растительности',
        help_text='Оценка от 1 до 10'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Путешествие'
        verbose_name_plural = 'Путешествия'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.location}"
