from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.dispatch import receiver
from .models import FraudEvent

@receiver(user_login_failed)
def log_failed_login(sender, credentials, request, **kwargs):
    if request:
        FraudEvent.objects.create(
            user=None,
            event_type="FAILED_LOGIN",
            risk_score=20,
            ip_address=request.META.get("REMOTE_ADDR"),
            metadata={"username": credentials.get("username")}
        )
