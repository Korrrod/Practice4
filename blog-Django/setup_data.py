import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Post, Tag, Follow

users = [
    {'username': 'alice',  'password': 'pass123', 'first_name': 'Алиса', 'email': 'alice@example.com'},
    {'username': 'oleg',   'password': 'pass123', 'first_name': 'Олег',  'email': 'oleg@example.com'},
    {'username': 'maria',  'password': 'pass123', 'first_name': 'Мария', 'email': 'maria@example.com'},
]

created_users = {}
for u in users:
    user, created = User.objects.get_or_create(username=u['username'])
    if created:
        user.set_password(u['password'])
        user.first_name = u['first_name']
        user.email = u['email']
        user.save()
    created_users[u['username']] = user

posts = [
    {
        'author': 'alice',
        'title': 'Первый пост Алисы',
        'content': 'Первый пост. Видимость — публичная, теги — Первый тег и Второй тег. Любой пользователь может прочитать этот пост.',
        'visibility': 'public',
        'tags': ['Первый тег', 'Второй тег'],
    },
    {
        'author': 'alice',
        'title': 'Второй пост Алисы',
        'content': 'Второй пост. Видимость — публичная, тег — Второй тег. Текст и теги можно изменить при редактировании.',
        'visibility': 'public',
        'tags': ['Второй тег'],
    },
    {
        'author': 'oleg',
        'title': 'Первый пост Олега',
        'content': 'Первый пост. Видимость — публичная, тег — Первый тег. Пост доступен всем без входа в систему.',
        'visibility': 'public',
        'tags': ['Первый тег'],
    },
    {
        'author': 'oleg',
        'title': 'Второй пост Олега',
        'content': 'Второй пост. Видимость — публичная, теги — Второй тег и Третий тег. Теги кликабельны — по ним можно найти все посты с этим тегом.',
        'visibility': 'public',
        'tags': ['Второй тег', 'Третий тег'],
    },
    {
        'author': 'maria',
        'title': 'Первый пост Марии',
        'content': 'Первый пост. Видимость — только для подписчиков. Посмотреть его могут только те, кто подписан на автора.',
        'visibility': 'subscribers',
        'tags': ['Первый тег'],
    },
    {
        'author': 'maria',
        'title': 'Второй пост Марии',
        'content': 'Второй пост. Видимость — публичная, теги — Первый тег и Третий тег.',
        'visibility': 'public',
        'tags': ['Первый тег', 'Третий тег'],
    },
]

for p in posts:
    author = created_users[p['author']]
    if not Post.objects.filter(author=author, title=p['title']).exists():
        post = Post.objects.create(
            author=author,
            title=p['title'],
            content=p['content'],
            visibility=p['visibility'],
        )
        for tag_name in p['tags']:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            post.tags.add(tag)

Follow.objects.get_or_create(follower=created_users['oleg'],  following=created_users['alice'])
Follow.objects.get_or_create(follower=created_users['maria'], following=created_users['alice'])
Follow.objects.get_or_create(follower=created_users['alice'], following=created_users['oleg'])

print('Done')
