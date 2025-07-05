from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from graduation_backend.settings.base import DEFAULT_FROM_EMAIL

User = get_user_model()

@shared_task
def send_verification_email_task(email, otp):
    send_mail(
        'Verify your email',
        f'Please verify your email: {otp}',
        DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )

@shared_task
def send_reset_password_verification_email_task(email, otp):
    send_mail(
        'Reset Password',
        f'OTP for resetting your password: {otp}',
        DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )