# admin.py

from django.contrib import admin
from .models import CustomUser, Seat, Booking

class BookingInline(admin.TabularInline):  # или admin.StackedInline
    model = Booking
    extra = 0  # Не показывать пустые поля для новых записей
    can_delete = True  # Разрешить удаление
    readonly_fields = ('seat', 'booking_date')  # Только чтение для полей


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'full_name', 'birth_date')
    search_fields = ('username', 'email', 'full_name')
    list_filter = ('date_joined',)
    ordering = ('-date_joined',)

    inlines = [BookingInline]  # Теперь брони будут отображаться и удаляться здесь



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

    # Добавляем действие "Удалить выбранные"
    actions = ['delete_selected']

    def delete_selected(self, request, queryset):
        """
        Удаляет выбранные брони и освобождает места.
        """
        for booking in queryset:
            seat = booking.seat
            seat.is_booked = False
            seat.save()
        queryset.delete()

    delete_selected.short_description = "Удалить выбранные брони"