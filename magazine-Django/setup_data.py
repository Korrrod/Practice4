import os
import django
from datetime import datetime, timezone as tz

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookstore.settings')
django.setup()

from django.contrib.auth.models import User
from library.models import Author, Category, Book, Rental, Purchase

# Очищаем старые данные
Rental.objects.all().delete()
Purchase.objects.all().delete()
Book.objects.all().delete()
Author.objects.all().delete()
Category.objects.all().delete()
User.objects.filter(is_superuser=False).delete()

# Создаём пользователей
admin = User.objects.create_user(username='admin', password='admin123', first_name='Админ', is_staff=True)
alice = User.objects.create_user(username='alice', password='pass123', first_name='Алиса', last_name='')
oleg = User.objects.create_user(username='oleg', password='pass123', first_name='Олег', last_name='')

# Создаём категорию
category = Category.objects.create(name='Классика', description='Классическая литература')

# Создаём авторов
keyes = Author.objects.create(name='Дэниел Киз', bio='Американский писатель-фантаст')
fitzgerald = Author.objects.create(name='Фрэнсис Скотт Фицджеральд', bio='Американский писатель')
dostoevsky = Author.objects.create(name='Фёдор Достоевский', bio='Русский писатель и мыслитель')

# Создаём книги
book1 = Book.objects.create(
    title='Цветы для Элджернона',
    author=keyes,
    category=category,
    year=1966,
    description='История об умственно отсталом молодом человеке, который стал участником эксперимента по повышению интеллекта.',
    price=450,
    rental_price_2weeks=100,
    rental_price_1month=180,
    rental_price_3months=300,
    status='rented',
)

book2 = Book.objects.create(
    title='Великий Гэтсби',
    author=fitzgerald,
    category=category,
    year=1925,
    description='История о богаче Джее Гэтсби и его стремлении вернуть прошлое ради потерянной любви.',
    price=380,
    rental_price_2weeks=90,
    rental_price_1month=160,
    rental_price_3months=270,
    status='sold',
)

book3 = Book.objects.create(
    title='Преступление и наказание',
    author=dostoevsky,
    category=category,
    year=1866,
    description='Роман о студенте Раскольникове, совершившем убийство и терзаемом муками совести.',
    price=420,
    rental_price_2weeks=95,
    rental_price_1month=170,
    rental_price_3months=280,
    status='available',
)

# Алиса арендует "Цветы для Элджернона" с 01.01.2026 (просрочена)
rental = Rental.objects.create(
    user=alice,
    book=book1,
    period='1month',
    price=book1.rental_price_1month,
    end_date=datetime(2026, 2, 1, tzinfo=tz.utc),
)
Rental.objects.filter(pk=rental.pk).update(start_date=datetime(2026, 1, 1, tzinfo=tz.utc))

# Алиса ранее брала "Преступление и наказание" и вернула
rental2 = Rental.objects.create(
    user=alice,
    book=book3,
    period='2weeks',
    price=book3.rental_price_2weeks,
    is_active=False,
    end_date=datetime(2025, 11, 14, tzinfo=tz.utc),
)
Rental.objects.filter(pk=rental2.pk).update(start_date=datetime(2025, 11, 1, tzinfo=tz.utc))

# Олег ранее брал "Преступление и наказание" и вернул
rental3 = Rental.objects.create(
    user=oleg,
    book=book3,
    period='1month',
    price=book3.rental_price_1month,
    is_active=False,
    end_date=datetime(2025, 12, 15, tzinfo=tz.utc),
)
Rental.objects.filter(pk=rental3.pk).update(start_date=datetime(2025, 11, 15, tzinfo=tz.utc))

# Олег покупает "Великий Гэтсби"
Purchase.objects.create(
    user=oleg,
    book=book2,
    price=book2.price,
)

print('Done! Users, books and transactions created.')
print('alice / pass123')
print('oleg  / pass123')
