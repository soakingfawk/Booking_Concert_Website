from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('verify-email/', views.verify_email, name='verify_email'),
    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('password-reset/verify/', views.password_reset_verify, name='password_reset_verify'),
    path('password-reset/new/', views.password_reset_new, name='password_reset_new'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('book/', views.book_seat, name='book_seat'),
    path('ajax/book_seat/', views.ajax_book_seat, name='ajax_book_seat'),
    path('ajax/delete_booking/', views.ajax_delete_booking, name='ajax_delete_booking'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('booking/<int:booking_id>/', views.booking_detail, name='booking_detail'),
]