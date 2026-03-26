import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_project.settings')
django.setup()

from django.contrib.auth.models import User
from travels.models import Travel

# Пользователи
users_data = [
    {'username': 'alice', 'first_name': 'Алиса', 'password': 'pass123'},
    {'username': 'oleg',  'first_name': 'Олег',  'password': 'pass123'},
    {'username': 'maria', 'first_name': 'Мария', 'password': 'pass123'},
]

users = {}
for u in users_data:
    user, created = User.objects.get_or_create(username=u['username'])
    if created:
        user.first_name = u['first_name']
        user.set_password(u['password'])
        user.save()
        print(f'[OK] Создан пользователь: {u["username"]}')
    else:
        print(f'[--] Уже существует: {u["username"]}')
    users[u['username']] = user

# Путешествия
travels_data = [
    {
        'user': 'alice',
        'title': 'Путешествие по Японии',
        'description': 'Незабываемая поездка в страну восходящего солнца. Посетила Токио, Киото и Осаку.',
        'location': 'Япония',
        'cost': 150000,
        'year': 2019,
        'places_to_visit': 'Токио, Киото, Осака, гора Фудзи',
        'transport_rating': 9,
        'safety_rating': 10,
        'population_rating': 8,
        'vegetation_rating': 7,
    },
    {
        'user': 'alice',
        'title': 'Отдых в Таиланде',
        'description': 'Пляжный отдых на островах Пхукет и Самуи. Тёплое море и экзотическая еда.',
        'location': 'Таиланд',
        'cost': 80000,
        'year': 2022,
        'places_to_visit': 'Пхукет, Самуи, Бангкок, храм Ват Пхо',
        'transport_rating': 6,
        'safety_rating': 7,
        'population_rating': 9,
        'vegetation_rating': 9,
    },
    {
        'user': 'oleg',
        'title': 'Горный поход по Кавказу',
        'description': 'Трёхнедельный поход по горным тропам Кавказа. Ночёвки в палатках, виды на Эльбрус.',
        'location': 'Россия, Кавказ',
        'cost': 30000,
        'year': 2018,
        'places_to_visit': 'Приэльбрусье, Домбай, Архыз, перевал Клухор',
        'transport_rating': 5,
        'safety_rating': 6,
        'population_rating': 3,
        'vegetation_rating': 10,
    },
    {
        'user': 'oleg',
        'title': 'Европейский тур',
        'description': 'Две недели по Европе: Германия, Австрия, Чехия. Ездил на поезде между городами.',
        'location': 'Европа',
        'cost': 120000,
        'year': 2021,
        'places_to_visit': 'Берлин, Вена, Прага, Зальцбург',
        'transport_rating': 9,
        'safety_rating': 9,
        'population_rating': 8,
        'vegetation_rating': 7,
    },
    {
        'user': 'maria',
        'title': 'Сафари в Кении',
        'description': 'Невероятное сафари в национальном парке Масаи Мара. Видела большую пятёрку.',
        'location': 'Кения',
        'cost': 200000,
        'year': 2023,
        'places_to_visit': 'Масаи Мара, Найроби, озеро Накуру',
        'transport_rating': 5,
        'safety_rating': 6,
        'population_rating': 4,
        'vegetation_rating': 8,
    },
    {
        'user': 'maria',
        'title': 'Путешествие по Италии',
        'description': 'Классический тур по Италии: Рим, Флоренция, Венеция. Вкусная еда и много архитектуры.',
        'location': 'Италия',
        'cost': 110000,
        'year': 2024,
        'places_to_visit': 'Рим, Флоренция, Венеция, Колизей, галерея Уффици',
        'transport_rating': 7,
        'safety_rating': 8,
        'population_rating': 9,
        'vegetation_rating': 6,
    },
]

for t in travels_data:
    user = users[t['user']]
    exists = Travel.objects.filter(user=user, title=t['title']).exists()
    if not exists:
        Travel.objects.create(
            user=user,
            title=t['title'],
            description=t['description'],
            location=t['location'],
            cost=t['cost'],
            year=t['year'],
            places_to_visit=t['places_to_visit'],
            transport_rating=t['transport_rating'],
            safety_rating=t['safety_rating'],
            population_rating=t['population_rating'],
            vegetation_rating=t['vegetation_rating'],
        )
        print(f'[OK] Создано путешествие: {t["title"]} ({t["user"]})')
    else:
        print(f'[--] Уже существует: {t["title"]}')

print('\nГотово.')
