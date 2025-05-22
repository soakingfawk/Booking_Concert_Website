# utils.py
from django.core.mail import send_mail
import random

def send_verification_code(user):
    code = str(random.randint(100000, 999999))
    user.verification_code = code
    user.save()

    send_mail(
        subject='Подтверждение регистрации',
        message=f'Ваш код подтверждения: {code}',
        from_email='drnikita2005@mail.ru',  # Укажи актуальный email
        recipient_list=[user.email],
        fail_silently=False,
    )

def send_reset_code(user):
    code = str(random.randint(100000, 999999))
    user.reset_code = code
    user.save()
    send_mail(
        'Код сброса пароля',
        f'Ваш код сброса пароля: {code}',
        'drnikita2005@mail.ru',
        [user.email],
        fail_silently=False,
    )