from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from datetime import date, datetime

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label="Email")

class PasswordResetVerifyForm(forms.Form):
    verification_code = forms.CharField(max_length=6, label="Код подтверждения")

class SetNewPasswordForm(forms.Form):
    new_password1 = forms.CharField(widget=forms.PasswordInput, label="Новый пароль")
    new_password2 = forms.CharField(widget=forms.PasswordInput, label="Подтверждение пароля")

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('new_password1') != cleaned_data.get('new_password2'):
            raise forms.ValidationError("Пароли не совпадают")
        return cleaned_data

class RegisterForm(UserCreationForm):
    full_name = forms.CharField(max_length=255, label="ФИО")
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Дата рождения")
    email = forms.EmailField(label="Электронная почта")
    avatar = forms.ImageField(
        required=False,  # Поле необязательное
        label="Аватар",
        widget=forms.FileInput(attrs={'accept': 'image/*'})  # Разрешаем только изображения
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'full_name', 'birth_date', 'email', 'password1', 'password2', 'avatar']

class LoginForm(forms.Form):
    username = forms.CharField(label="Имя пользователя")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

class ProfileForm(forms.ModelForm):
    birth_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'min': '1900-01-01',
                'max': date.today().isoformat()
            },
            format='%Y-%m-%d'
        ),
        label="Дата рождения",
        input_formats=['%Y-%m-%d']
    )

    avatar = forms.ImageField(
        required=False,
        label="Аватар",
        widget=forms.FileInput(attrs={'accept': 'image/*'})
    )

    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'birth_date', 'avatar']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError("Этот email уже используется другим пользователем.")
        return email

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        min_date = date(1900, 1, 1)
        if birth_date:
            if birth_date < min_date:
                raise forms.ValidationError("Дата рождения не может быть ранее 01.01.1900.")
            if birth_date > date.today():
                raise forms.ValidationError("Дата рождения не может быть в будущем.")
        return birth_date