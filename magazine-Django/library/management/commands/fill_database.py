from django.core.management.base import BaseCommand
from library.models import Author, Category, Book


class Command(BaseCommand):
    help = 'Заполняет базу данных авторами, категориями и книгами'

    def handle(self, *args, **options):
        # Создаем категории
        categories_data = [
            {'name': 'Фантастика', 'description': 'Научная фантастика и фэнтези'},
            {'name': 'Детектив', 'description': 'Детективные романы и триллеры'},
            {'name': 'Роман', 'description': 'Романтические произведения'},
            {'name': 'Классика', 'description': 'Классическая литература'},
            {'name': 'Приключения', 'description': 'Приключенческие романы'},
        ]
        
        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(self.style.SUCCESS(f'Создана категория: {category.name}'))
        
        # Создаем авторов и их книги
        authors_books = [
            {
                'author': {'name': 'Лев Толстой', 'bio': 'Русский писатель, классик мировой литературы', 'birth_date': '1828-09-09'},
                'books': [
                    {
                        'title': 'Война и мир',
                        'year': 1869,
                        'category': 'Классика',
                        'description': 'Эпический роман о войне 1812 года и жизни русского общества начала XIX века. Одно из величайших произведений мировой литературы.',
                        'price': 1500.00,
                        'rental_price_2weeks': 200.00,
                        'rental_price_1month': 350.00,
                        'rental_price_3months': 900.00,
                    },
                    {
                        'title': 'Анна Каренина',
                        'year': 1877,
                        'category': 'Классика',
                        'description': 'Трагическая история любви замужней дамы Анны Карениной и блестящего офицера Вронского на фоне жизни высшего общества.',
                        'price': 1200.00,
                        'rental_price_2weeks': 180.00,
                        'rental_price_1month': 300.00,
                        'rental_price_3months': 750.00,
                    },
                    {
                        'title': 'Воскресение',
                        'year': 1899,
                        'category': 'Классика',
                        'description': 'Последний роман Толстого о нравственном возрождении человека и критике судебной системы.',
                        'price': 1000.00,
                        'rental_price_2weeks': 150.00,
                        'rental_price_1month': 250.00,
                        'rental_price_3months': 600.00,
                    },
                ]
            },
            {
                'author': {'name': 'Фёдор Достоевский', 'bio': 'Русский писатель, философ, публицист', 'birth_date': '1821-11-11'},
                'books': [
                    {
                        'title': 'Преступление и наказание',
                        'year': 1866,
                        'category': 'Классика',
                        'description': 'Психологический роман о студенте Раскольникове, который совершает убийство и переживает муки совести.',
                        'price': 1300.00,
                        'rental_price_2weeks': 190.00,
                        'rental_price_1month': 320.00,
                        'rental_price_3months': 800.00,
                    },
                    {
                        'title': 'Идиот',
                        'year': 1869,
                        'category': 'Классика',
                        'description': 'Роман о князе Мышкине, человеке необычайной доброты и чистоты, который пытается жить в жестоком мире.',
                        'price': 1250.00,
                        'rental_price_2weeks': 185.00,
                        'rental_price_1month': 310.00,
                        'rental_price_3months': 780.00,
                    },
                    {
                        'title': 'Братья Карамазовы',
                        'year': 1880,
                        'category': 'Классика',
                        'description': 'Последний роман Достоевского о трёх братьях Карамазовых и их отце, затрагивающий вопросы веры, морали и свободы.',
                        'price': 1400.00,
                        'rental_price_2weeks': 210.00,
                        'rental_price_1month': 360.00,
                        'rental_price_3months': 900.00,
                    },
                ]
            },
            {
                'author': {'name': 'Агата Кристи', 'bio': 'Английская писательница, мастер детективного жанра', 'birth_date': '1890-09-15'},
                'books': [
                    {
                        'title': 'Убийство в Восточном экспрессе',
                        'year': 1934,
                        'category': 'Детектив',
                        'description': 'Знаменитый детектив Эркюль Пуаро расследует убийство в поезде, застрявшем в снегу. Все пассажиры под подозрением.',
                        'price': 800.00,
                        'rental_price_2weeks': 120.00,
                        'rental_price_1month': 200.00,
                        'rental_price_3months': 500.00,
                    },
                    {
                        'title': 'Десять негритят',
                        'year': 1939,
                        'category': 'Детектив',
                        'description': 'Десять человек приглашены на остров, где их начинают убивать одного за другим согласно детской считалке.',
                        'price': 750.00,
                        'rental_price_2weeks': 110.00,
                        'rental_price_1month': 180.00,
                        'rental_price_3months': 450.00,
                    },
                    {
                        'title': 'Смерть на Ниле',
                        'year': 1937,
                        'category': 'Детектив',
                        'description': 'Пуаро расследует убийство богатой наследницы во время круиза по Нилу. Все подозреваемые имеют мотив.',
                        'price': 850.00,
                        'rental_price_2weeks': 130.00,
                        'rental_price_1month': 220.00,
                        'rental_price_3months': 550.00,
                    },
                ]
            },
            {
                'author': {'name': 'Джордж Оруэлл', 'bio': 'Английский писатель и публицист', 'birth_date': '1903-06-25'},
                'books': [
                    {
                        'title': '1984',
                        'year': 1949,
                        'category': 'Фантастика',
                        'description': 'Антиутопический роман о тоталитарном обществе, где за каждым следят, а независимое мышление преследуется.',
                        'price': 900.00,
                        'rental_price_2weeks': 140.00,
                        'rental_price_1month': 240.00,
                        'rental_price_3months': 600.00,
                    },
                    {
                        'title': 'Скотный двор',
                        'year': 1945,
                        'category': 'Фантастика',
                        'description': 'Сатирическая повесть-притча о животных, которые свергают своих хозяев и создают собственное государство.',
                        'price': 700.00,
                        'rental_price_2weeks': 100.00,
                        'rental_price_1month': 170.00,
                        'rental_price_3months': 420.00,
                    },
                    {
                        'title': 'Памяти Каталонии',
                        'year': 1938,
                        'category': 'Приключения',
                        'description': 'Автобиографическая книга о пребывании Оруэлла в Испании во время Гражданской войны.',
                        'price': 650.00,
                        'rental_price_2weeks': 95.00,
                        'rental_price_1month': 160.00,
                        'rental_price_3months': 400.00,
                    },
                ]
            },
            {
                'author': {'name': 'Жюль Верн', 'bio': 'Французский писатель, основоположник научной фантастики', 'birth_date': '1828-02-08'},
                'books': [
                    {
                        'title': 'Двадцать тысяч лье под водой',
                        'year': 1870,
                        'category': 'Фантастика',
                        'description': 'Приключенческий роман о капитане Немо и его подводной лодке "Наутилус", путешествующей по морям и океанам.',
                        'price': 950.00,
                        'rental_price_2weeks': 145.00,
                        'rental_price_1month': 250.00,
                        'rental_price_3months': 630.00,
                    },
                    {
                        'title': 'Вокруг света за 80 дней',
                        'year': 1873,
                        'category': 'Приключения',
                        'description': 'Захватывающее путешествие Филеаса Фогга и его слуги Паспарту вокруг земного шара за 80 дней.',
                        'price': 850.00,
                        'rental_price_2weeks': 130.00,
                        'rental_price_1month': 220.00,
                        'rental_price_3months': 550.00,
                    },
                    {
                        'title': 'Путешествие к центру Земли',
                        'year': 1864,
                        'category': 'Приключения',
                        'description': 'Фантастическая история о путешествии профессора Лиденброка и его племянника к центру Земли через вулкан.',
                        'price': 880.00,
                        'rental_price_2weeks': 135.00,
                        'rental_price_1month': 230.00,
                        'rental_price_3months': 580.00,
                    },
                ]
            },
        ]
        
        # Создаем авторов и книги
        for author_data in authors_books:
            author_info = author_data['author']
            author, created = Author.objects.get_or_create(
                name=author_info['name'],
                defaults={
                    'bio': author_info['bio'],
                    'birth_date': author_info['birth_date']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Создан автор: {author.name}'))
            
            for book_data in author_data['books']:
                book, created = Book.objects.get_or_create(
                    title=book_data['title'],
                    author=author,
                    defaults={
                        'year': book_data['year'],
                        'category': categories[book_data['category']],
                        'description': book_data['description'],
                        'price': book_data['price'],
                        'rental_price_2weeks': book_data['rental_price_2weeks'],
                        'rental_price_1month': book_data['rental_price_1month'],
                        'rental_price_3months': book_data['rental_price_3months'],
                        'status': 'available',
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'  Создана книга: {book.title}'))
                else:
                    self.stdout.write(self.style.WARNING(f'  Книга уже существует: {book.title}'))
        
        self.stdout.write(self.style.SUCCESS('\nБаза данных успешно заполнена!'))
        self.stdout.write(self.style.SUCCESS(f'Создано авторов: {Author.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Создано категорий: {Category.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Создано книг: {Book.objects.count()}'))

