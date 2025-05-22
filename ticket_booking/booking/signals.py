from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Booking, Seat

@receiver(post_delete, sender=Booking)
def release_seat_on_booking_delete(sender, instance, **kwargs):
    """
    Когда бронь удаляется, освобождаем соответствующее место
    """
    seat = instance.seat
    seat.is_booked = False
    seat.save()