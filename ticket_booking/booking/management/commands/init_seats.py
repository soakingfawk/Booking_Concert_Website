from django.core.management.base import BaseCommand
from booking.models import Seat

class Command(BaseCommand):
    help = 'Initialize seats for booking (Balcony: 148 seats, Parterre: 445 seats)'

    def handle(self, *args, **kwargs):
        Seat.objects.all().delete()  # Очищаем существующие места

        # Балкон: 7 рядов
        # Ряд 7: 28 мест (1–14, 15–28)
        for number in range(1, 29):
            Seat.objects.create(section='Balcony', row=7, number=number, is_booked=False)
        # Ряды 1–6: 20 мест (1–10, 11–20)
        for row in range(1, 7):
            for number in range(1, 21):
                Seat.objects.create(section='Balcony', row=row, number=number, is_booked=False)

        # Партер: 20 рядов
        # Ряд 20: 11 мест (16–26)
        for number in range(16, 27):
            Seat.objects.create(section='Parterre', row=20, number=number, is_booked=False)
        # Ряды 1–19: разное количество мест
        parterre_rows = [
            (19, range(1, 13), range(15, 25)),  # 22 места
            (18, range(1, 13), range(13, 25)),  # 24 места
            (17, range(1, 13), range(13, 25)),  # 24 места
            (16, range(1, 13), range(13, 25)),  # 24 места
            (15, range(1, 13), range(13, 25)),  # 24 места
            (14, range(1, 13), range(13, 25)),  # 24 места
            (13, range(1, 13), range(13, 25)),  # 24 места
            (12, range(1, 13), range(13, 25)),  # 24 места
            (11, range(1, 13), range(13, 25)),  # 24 места
            (10, range(1, 13), range(13, 25)),  # 24 места
            (9, range(1, 13), range(13, 25)),   # 24 места
            (8, range(1, 13), range(13, 25)),   # 24 места
            (7, range(1, 13), range(13, 25)),   # 24 места
            (6, range(1, 13), range(13, 25)),   # 24 места
            (5, range(1, 13), range(13, 25)),   # 24 места
            (4, range(1, 12), range(12, 23)),   # 22 места
            (3, range(1, 11), range(11, 21)),   # 20 мест
            (2, range(1, 10), range(10, 19)),   # 18 мест
            (1, range(1, 9), range(9, 17)),     # 16 мест
        ]
        for row, left_range, right_range in parterre_rows:
            for number in left_range:
                Seat.objects.create(section='Parterre', row=row, number=number, is_booked=False)
            for number in right_range:
                Seat.objects.create(section='Parterre', row=row, number=number, is_booked=False)

        self.stdout.write(self.style.SUCCESS(f'Successfully initialized {Seat.objects.count()} seats'))