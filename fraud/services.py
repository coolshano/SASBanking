from datetime import timedelta
from django.utils import timezone
from .models import FraudEvent

# -----------------------------
# LOGIN FRAUD DETECTION
# -----------------------------
def detect_login_fraud(user, ip_address):
    recent_failures = FraudEvent.objects.filter(
        user=user,
        event_type="FAILED_LOGIN",
        created_at__gte=timezone.now() - timedelta(minutes=5)
    ).count()

    if recent_failures >= 5:
        return 80  # High risk

    return 0


# -----------------------------
# OTP FRAUD DETECTION
# -----------------------------
def detect_otp_fraud(user, ip_address):
    otp_failures = FraudEvent.objects.filter(
        user=user,
        event_type="OTP_FAILURE",
        created_at__gte=timezone.now() - timedelta(minutes=10)
    ).count()

    if otp_failures >= 3:
        return 70

    return 0


# -----------------------------
# TRANSACTION FRAUD (FUTURE)
# -----------------------------
def detect_transaction_fraud(user, amount, avg_amount):
    if avg_amount and amount > avg_amount * 5:
        return 90

    return 0
