from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from library.models import Rental
from datetime import timedelta


class Command(BaseCommand):
    help = 'Отправляет напоминания пользователям об окончании срока аренды'

    def handle(self, *args, **options):
        # Находим аренды, которые истекают в течение 3 дней и напоминание еще не отправлено
        three_days_from_now = timezone.now() + timedelta(days=3)
        expiring_rentals = Rental.objects.filter(
            is_active=True,
            end_date__lte=three_days_from_now,
            end_date__gte=timezone.now(),
            reminder_sent=False
        )

        count = 0
        for rental in expiring_rentals:
            # В реальном приложении здесь была бы отправка email или уведомления
            # Для демонстрации просто помечаем, что напоминание отправлено
            rental.reminder_sent = True
            rental.save()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Напоминание отправлено пользователю {rental.user.username} '
                    f'о книге "{rental.book.title}" (истекает {rental.end_date.strftime("%d.%m.%Y")})'
                )
            )
            count += 1

        # Также отправляем напоминания о просроченных арендах
        expired_rentals = Rental.objects.filter(
            is_active=True,
            end_date__lt=timezone.now(),
            reminder_sent=False
        )

        for rental in expired_rentals:
            rental.reminder_sent = True
            rental.save()
            
            self.stdout.write(
                self.style.WARNING(
                    f'Напоминание о просрочке отправлено пользователю {rental.user.username} '
                    f'о книге "{rental.book.title}" (просрочена с {rental.end_date.strftime("%d.%m.%Y")})'
                )
            )
            count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Всего отправлено напоминаний: {count}')
        )


