from django.db.models.signals import post_save
from django.dispatch import receiver
from authentication.models import User
from authentication.tasks import send_verification_email_task
from authentication.utils import generate_random_otp

#time
from django.utils import timezone

@receiver(post_save, sender=User)
def send_verification_email_signal(sender, instance, created, **kwargs):
    if created:
        otp = generate_random_otp()
        instance.otp = otp
        instance.otp_exp = timezone.now()
        instance.save()
        send_verification_email_task.delay(instance.email, otp)