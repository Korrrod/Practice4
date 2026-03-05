from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):

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

    def __str__(self):
        return self.title

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


class Follow(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f'{self.follower} подписан на {self.following}'


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

    def __str__(self):
        return f'{self.requester} запрашивает доступ к "{self.post}"'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Комментарий от {self.author} к "{self.post}"'
