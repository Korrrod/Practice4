from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Travel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='travels', verbose_name='Пользователь')
    title = models.CharField(max_length=200, verbose_name='Название путешествия')
    description = models.TextField(verbose_name='Описание')
    location = models.CharField(max_length=200, verbose_name='Местоположение')
    image = models.ImageField(upload_to='travel_images/', blank=True, null=True, verbose_name='Изображение')
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость путешествия')
    places_to_visit = models.TextField(verbose_name='Места для посещения')
    transport_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Оценка удобства передвижения'
    )
    safety_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Оценка безопасности'
    )
    population_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Оценка населенности'
    )
    vegetation_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Оценка растительности'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Путешествие'
        verbose_name_plural = 'Путешествия'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.location}"
