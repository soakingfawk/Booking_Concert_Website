from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from .models import Seat, Booking
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('booking:profile')
    else:
        form = RegisterForm()
    return render(request, 'booking/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                return redirect('booking:profile')
    else:
        form = LoginForm()
    return render(request, 'booking/login.html', {'form': form})

def user_logout(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('booking:home')

def home(request):
    return render(request, 'booking/home.html')

@login_required
def profile(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'booking/profile.html', {'bookings': bookings})

@login_required
def book_seat(request):
    balcony_seats = Seat.objects.filter(section='Balcony').order_by('-row', 'number')
    balcony_rows = []
    for row in range(7, 0, -1):
        row_seats = balcony_seats.filter(row=row)
        if row_seats.exists():
            balcony_rows.append((row, row_seats))

    parterre_seats = Seat.objects.filter(section='Parterre').order_by('-row', 'number')
    parterre_rows = []
    for row in range(20, 0, -1):
        row_seats = parterre_seats.filter(row=row)
        if row_seats.exists():
            if 17 <= row <= 18:  # Для рядов с 18 по 17
                left_seats_count = 12
                right_seats_count = 12
                left_shift = -23 # Пример сдвига левой секции
                right_shift = 73 # Пример сдвига правой секции
                margin_bottom = 0  # Без промежутка
                horizontal_shift = -75
            else:
                if 15 <= row <= 16:  # Для рядов с 16 по 5
                    left_seats_count = 12
                    right_seats_count = 12
                    left_shift = -23  # Пример сдвига левой секции
                    right_shift = 25  # Пример сдвига правой секции
                    margin_bottom = 0  # Без промежутка
                    horizontal_shift = -75
                elif 5 <= row <= 12:  # Для рядов с 16 по 5
                    left_seats_count = 12
                    right_seats_count = 12
                    left_shift = -23  # Пример сдвига левой секции
                    right_shift = 25  # Пример сдвига правой секции
                    margin_bottom = 0  # Без промежутка
                    horizontal_shift = -75
                elif row == 14:
                    left_seats_count = 12
                    right_seats_count = 12
                    left_shift = -23  # Пример сдвига левой секции
                    right_shift = 25 # Пример сдвига правой секции
                    margin_bottom = 30  # Промежуток между 14 и 13 рядом
                    horizontal_shift = -75
                elif row == 13:
                    left_seats_count = 12
                    right_seats_count = 12
                    left_shift = -23  # Пример сдвига левой секции
                    right_shift = 25  # Пример сдвига правой секции
                    margin_bottom = 0  # Без промежутка
                    horizontal_shift = -75
                elif row == 19:
                    left_seats_count = 12
                    right_seats_count = 13
                    left_shift = -23
                    right_shift = 121
                    margin_bottom = 0  # Без промежутка
                    horizontal_shift = -75
                elif row == 20:
                    left_seats_count = 0
                    right_seats_count = 11
                    left_shift = 0
                    right_shift = 433
                    margin_bottom = 0  # Без промежутка
                    horizontal_shift = -50
                elif row == 4:
                    left_seats_count = 11
                    right_seats_count = 11
                    left_shift = -23
                    right_shift = 25
                    margin_bottom = 0  # Без промежутка
                    horizontal_shift = -75
                elif row == 3:
                    left_seats_count = 10
                    right_seats_count = 10
                    left_shift = -23
                    right_shift = 25
                    margin_bottom = 0  # Без промежутка
                    horizontal_shift = -75
                elif row == 2:
                    left_seats_count = 9
                    right_seats_count = 9
                    left_shift = -23
                    right_shift = 25
                    margin_bottom = 0  # Без промежутка
                    horizontal_shift = -75
                else:
                    left_seats_count = 8
                    right_seats_count = 8
                    left_shift = -23
                    right_shift = 25
                    margin_bottom = 0  # Без промежутка
                    horizontal_shift = -75

            left_seats = row_seats.filter(number__lte=left_seats_count).order_by('number')
            right_seats = row_seats.filter(number__gt=right_seats_count).order_by('number')

            parterre_rows.append((row, {
                'left': left_seats,
                'right': right_seats,
                'pass_gap': 0,
                'left_gap': 0,
                'left_shift': left_shift,
                'right_shift': right_shift,
                'margin_bottom': margin_bottom,  # Промежуток между рядами
                'horizontal_shift': horizontal_shift

            }))
    return render(request, 'booking/book_seat.html', {
        'balcony_rows': balcony_rows,
        'parterre_rows': parterre_rows,
    })

@csrf_exempt
@login_required
def ajax_book_seat(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            seat_id = data.get('seat_id')
            seat = Seat.objects.get(id=seat_id)
            if seat.is_booked:
                return JsonResponse({'status': 'error', 'message': 'Место уже забронировано'})
            Booking.objects.create(user=request.user, seat=seat)
            seat.is_booked = True
            seat.save()
            return JsonResponse({'status': 'success', 'message': 'Место успешно забронировано'})
        except Seat.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Место не найдено'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Неверный запрос'})

@csrf_exempt
@login_required
def ajax_delete_booking(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            booking_id = data.get('booking_id')
            booking = Booking.objects.get(id=booking_id, user=request.user)
            seat = booking.seat
            booking.delete()
            seat.is_booked = False
            seat.save()
            return JsonResponse({'status': 'success', 'message': 'Бронь успешно удалена'})
        except Booking.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Бронь не найдена'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Неверный запрос'})