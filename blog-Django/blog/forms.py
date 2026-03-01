from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Post, Comment


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': 'Логин',
            'email': 'Email',
            'password1': 'Пароль',
            'password2': 'Повтор пароля',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['email'].label = 'Email'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтверждение пароля'

        self.fields['username'].help_text = 'Используйте только буквы, цифры и @/./+/-/_.'
        self.fields['password1'].help_text = 'Минимум 8 символов, сложный пароль.'
        self.fields['password2'].help_text = 'Повторите пароль.'

        self.fields['username'].widget.attrs.update({'placeholder': 'Логин'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Пароль'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Повтор пароля'})


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'
        self.fields['username'].widget.attrs.update({'placeholder': 'Логин'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Пароль'})


class PostForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        label='Теги',
        help_text='Введите теги через запятую'
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'visibility', 'tags']
        labels = {
            'title': 'Заголовок',
            'content': 'Текст',
            'visibility': 'Видимость',
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Текст поста'}),
            'title': forms.TextInput(attrs={'placeholder': 'Заголовок поста'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {'content': 'Комментарий'}
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }


