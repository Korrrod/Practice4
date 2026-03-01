from django.conf import settings
from django.db import models
from django.utils.text import slugify


# Тег — метка для поста, например "путешествия" или "рецепты"
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)

    # Автоматически делаю slug из названия при сохранении (нужен для URL)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    # Как тег отображается в админке и при выводе
    def __str__(self):
        return self.name


# Пост — основная единица контента в блоге
class Post(models.Model):

    # Варианты видимости поста: для всех, только подписчики, по запросу
    class Visibility(models.TextChoices):
        PUBLIC = 'public', 'Публично'
        SUBSCRIBERS = 'subscribers', 'Только подписчики'
        ON_REQUEST = 'on_request', 'По запросу'

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    content = models.TextField()
    visibility = models.CharField(max_length=20, choices=Visibility.choices, default=Visibility.PUBLIC)
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)

    class Meta:
        ordering = ['-id']

    # Как пост отображается в админке и при выводе
    def __str__(self):
        return self.title

    # Проверяю, может ли пользователь видеть этот пост
    def can_view(self, user):
        if self.visibility == self.Visibility.PUBLIC:
            return True
        if not user.is_authenticated:
            return False
        if self.visibility == self.Visibility.SUBSCRIBERS:
            return Follow.objects.filter(follower=user, following=self.author).exists() or user == self.author
        if self.visibility == self.Visibility.ON_REQUEST:
            if user == self.author:
                return True
            return AccessRequest.objects.filter(post=self, requester=user, status='approved').exists()
        return False


# Подписка — связь между двумя пользователями
class Follow(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    # Как подписка отображается в админке
    def __str__(self):
        return f'{self.follower} подписан на {self.following}'


# Запрос на доступ к посту с видимостью "по запросу"
class AccessRequest(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='access_requests')
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='access_requests')
    status = models.CharField(max_length=20, default='pending', choices=[
        ('pending', 'Ожидает'),
        ('approved', 'Одобрен'),
        ('rejected', 'Отклонён'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'requester')

    # Как запрос отображается в админке
    def __str__(self):
        return f'{self.requester} запрашивает доступ к "{self.post}"'


# Комментарий к посту
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    # Как комментарий отображается в админке
    def __str__(self):
        return f'Комментарий от {self.author} к "{self.post}"'
