from datetime import timedelta
from django.utils import timezone
from .models import FraudEvent
from math import radians, sin, cos, sqrt, atan2

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



# Haversine distance (km)
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def detect_geo_anomaly(user, current_location):
    last_event = FraudEvent.objects.filter(
        user=user,
        metadata__isnull=False
    ).order_by("-created_at").first()

    if not last_event or not last_event.metadata:
        return 0

    prev = last_event.metadata

    # Country change
    if prev.get("country") != current_location.get("country"):
        return 60

    # Impossible travel (over 500km in <10 minutes)
    time_diff = timezone.now() - last_event.created_at
    if time_diff < timedelta(minutes=10):
        distance = calculate_distance(
            prev["lat"], prev["lon"],
            current_location["lat"], current_location["lon"]
        )

        if distance > 500:
            return 90

    return 0
