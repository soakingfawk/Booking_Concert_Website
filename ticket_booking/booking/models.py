from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.utils import timezone

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    reset_code = models.CharField(max_length=6, blank=True)

    avatar = models.ImageField(
        upload_to='avatars/',  # Папка для хранения аватаров
        blank=True,  # Разрешаем пустое значение
        null=True,  # Разрешаем NULL в базе данных
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]  # Разрешенные форматы
    )

    def __str__(self):
        return self.username

class Seat(models.Model):
    SECTION_CHOICES = [
        ('Balcony', 'Балкон'),
        ('Parterre', 'Партер'),
    ]
    section = models.CharField(max_length=20, choices=SECTION_CHOICES)
    row = models.IntegerField()
    number = models.IntegerField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.section}: Ряд {self.row}, Место {self.number}"

class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.seat}"

class TemporaryBanIp(models.Model):
    ip_address = models.GenericIPAddressField("IP адрес", unique=True)
    attempts = models.PositiveIntegerField("Неудачные попытки", default=0)
    time_unblock = models.DateTimeField("Время разблокировки", default=timezone.now)
    status = models.BooleanField("Статус блокировки", default=False)

    def __str__(self):
        return f"{self.ip_address} | {self.attempts} попыток"

    @classmethod
    def is_blocked(cls, ip_address):
        """
        Проверяет, заблокирован ли IP.
        """
        try:
            obj = cls.objects.get(ip_address=ip_address)
            if obj.status and obj.time_unblock > timezone.now():
                return True
            elif obj.time_unblock <= timezone.now():
                # Сбрасываем блокировку
                obj.status = False
                obj.save()
            return False
        except cls.DoesNotExist:
            return False

    @classmethod
    def register_attempt(cls, ip_address):
        """
        Регистрирует неудачную попытку и обновляет статус блокировки.
        """
        obj, created = cls.objects.get_or_create(ip_address=ip_address)

        obj.attempts += 1
        if obj.attempts in [3, 6]:
            obj.time_unblock = timezone.now() + timezone.timedelta(minutes=15)
            obj.status = True
        elif obj.attempts >= 9:
            obj.time_unblock = timezone.now() + timezone.timedelta(hours=24)
            obj.status = True
        obj.save()

        return obj