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
        'title': 'Как я начала вести блог',
        'content': 'Долго думала, стоит ли заводить блог. Решила попробовать — и не пожалела. Здесь буду писать о том, что интересно мне.',
        'visibility': 'public',
        'tags': ['блог', 'о себе'],
    },
    {
        'author': 'alice',
        'title': 'Любимые книги этого года',
        'content': 'Прочитала много всего, но выделю три книги, которые особенно запомнились. Первая — "Мастер и Маргарита". Вторая — "Дюна". Третья — "Три товарища".',
        'visibility': 'subscribers',
        'tags': ['книги', 'чтение'],
    },
    {
        'author': 'oleg',
        'title': 'Заметки о программировании',
        'content': 'Программирование — это не просто написание кода. Это решение задач. Иногда самое сложное — правильно понять задачу.',
        'visibility': 'public',
        'tags': ['программирование', 'мысли'],
    },
    {
        'author': 'oleg',
        'title': 'Почему я люблю Python',
        'content': 'Python читается как обычный текст. Можно объяснить код человеку, который никогда не программировал, и он поймёт общий смысл.',
        'visibility': 'public',
        'tags': ['python', 'программирование'],
    },
    {
        'author': 'maria',
        'title': 'Рецепт простого супа',
        'content': 'Беру картошку, морковь, лук и немного мяса. Варю около 40 минут. Добавляю соль и лавровый лист. Всё — суп готов.',
        'visibility': 'public',
        'tags': ['еда', 'рецепты'],
    },
    {
        'author': 'maria',
        'title': 'Прогулка по городу',
        'content': 'Вышла погулять без цели. Дошла до парка, посидела на лавочке, посмотрела на людей. Иногда это лучший способ отдохнуть.',
        'visibility': 'public',
        'tags': ['город', 'прогулки'],
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
