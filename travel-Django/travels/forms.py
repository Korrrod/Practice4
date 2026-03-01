from django import forms
from .models import Travel


class TravelForm(forms.ModelForm):
    class Meta:
        model = Travel
        fields = ['title', 'description', 'location', 'cost',
                  'places_to_visit', 'transport_rating', 'safety_rating',
                  'population_rating', 'vegetation_rating']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название путешествия'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Опишите ваше путешествие...'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Местоположение (город, страна)'
            }),
            'cost': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
            'places_to_visit': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Перечислите места для посещения...'
            }),
            'transport_rating': forms.NumberInput(attrs={
                'class': 'form-range',
                'type': 'range',
                'min': '1',
                'max': '10',
                'step': '1',
                'value': '5'
            }),
            'safety_rating': forms.NumberInput(attrs={
                'class': 'form-range',
                'type': 'range',
                'min': '1',
                'max': '10',
                'step': '1',
                'value': '5'
            }),
            'population_rating': forms.NumberInput(attrs={
                'class': 'form-range',
                'type': 'range',
                'min': '1',
                'max': '10',
                'step': '1',
                'value': '5'
            }),
            'vegetation_rating': forms.NumberInput(attrs={
                'class': 'form-range',
                'type': 'range',
                'min': '1',
                'max': '10',
                'step': '1',
                'value': '5'
            }),
        }
        labels = {
            'title': 'Название',
            'description': 'Описание',
            'location': 'Местоположение',
            'cost': 'Стоимость (руб.)',
            'places_to_visit': 'Места для посещения',
            'transport_rating': 'Удобство передвижения',
            'safety_rating': 'Безопасность',
            'population_rating': 'Населенность',
            'vegetation_rating': 'Растительность',
        }

