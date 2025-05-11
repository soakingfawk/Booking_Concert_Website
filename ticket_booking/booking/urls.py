from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('book/', views.book_seat, name='book_seat'),
    path('ajax/book_seat/', views.ajax_book_seat, name='ajax_book_seat'),
    path('ajax/delete_booking/', views.ajax_delete_booking, name='ajax_delete_booking'),
]