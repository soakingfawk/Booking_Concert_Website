# admin.py

from django.contrib import admin
from .models import CustomUser, Seat, Booking

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'full_name', 'birth_date')
    search_fields = ('username', 'email', 'full_name')
    list_filter = ('date_joined',)
    ordering = ('-date_joined',)

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('section', 'row', 'number', 'is_booked')
    list_filter = ('section', 'is_booked')
    search_fields = ('row', 'number')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'seat', 'booking_date')
    list_filter = ('booking_date', 'seat__section')
    search_fields = ('user__username', 'seat__section')