from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegisterForm(UserCreationForm):
    full_name = forms.CharField(max_length=255, label="ФИО")
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Дата рождения")
    email = forms.EmailField(label="Электронная почта")

    class Meta:
        model = CustomUser
        fields = ['username', 'full_name', 'birth_date', 'email', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField(label="Имя пользователя")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")