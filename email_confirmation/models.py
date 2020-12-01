import secrets
from datetime import timedelta

from django.db import models, IntegrityError
from django.conf import settings
from django.utils import timezone
from django.dispatch import receiver
from django.core.mail import send_mail
from django.urls import reverse


class EmailConfirmation(models.Model):
    token = models.CharField(max_length=64, primary_key=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="email_confirmation",
    )
    updated_at = models.DateTimeField(auto_now=True)

    def is_expired(self):
        now = timezone.now()
        limit = self.updated_at + timedelta(
            days=settings.EMAIL_CONFIRMATION_EXPIRATION_TIME
        )
        return now > limit

    def save(self, *args, **kwargs):
        if not self.token:
            while True:
                self.token = secrets.token_urlsafe(32)
                try:
                    repeated_token = EmailConfirmation.objects.get(token=self.token)
                    if repeated_token.is_expired():
                        repeated_token.delete()
                        raise EmailConfirmation.DoesNotExist
                except EmailConfirmation.DoesNotExist:
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return self.token

    def send_email_confirmation(self):
        send_mail(
            "Confirmação de Email",
            (
                f"Acesse o link abaixo para confirmar o seu e-mail.\n"
                f"{settings.SITE_URL}{reverse('token_validation')}?token={self.token}"
            ),
            settings.EMAIL_CONFIRMATION_FROM,
            [self.user.email],
            fail_silently=False,
        )


@receiver(models.signals.post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        EmailConfirmation.objects.create(user=instance).send_email_confirmation()
        instance.is_active = False
        instance.save()
