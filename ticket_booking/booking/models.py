from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    email = models.EmailField(unique=True)

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