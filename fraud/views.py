from django.shortcuts import render
from django.db.models import Count
from django.utils.timezone import now
from datetime import timedelta
import json
from django.core.serializers.json import DjangoJSONEncoder
from .models import FraudEvent
from django.contrib.auth.decorators import login_required


@login_required
def fraud_dashboard(request):
    last_7_days = now() - timedelta(days=7)

    total_events = FraudEvent.objects.count()

    failed_logins = FraudEvent.objects.filter(
        event_type="FAILED_LOGIN"
    ).count()

    otp_failures = FraudEvent.objects.filter(
        event_type="OTP_FAILURE"
    ).count()

    suspicious_logins = FraudEvent.objects.filter(
        event_type="SUSPICIOUS_LOGIN"
    ).count()

    # Events grouped by type
    events_by_type = (
        FraudEvent.objects
        .values("event_type")
        .annotate(count=Count("id"))
    )

    # Events over time (last 7 days)
    events_over_time = (
        FraudEvent.objects
        .filter(created_at__gte=last_7_days)
        .extra(select={'day': "date(created_at)"})
        .values("day")
        .annotate(count=Count("id"))
        .order_by("day")
    )

    # Top risky IPs
    
    top_ips = (
        FraudEvent.objects
        .exclude(metadata__isnull=True)
        .values(
            "ip_address",
            "metadata__location__country"
        )
        .annotate(count=Count("id"))
        .order_by("-count")[:5]
    )

    context = {
        "total_events": total_events,
        "failed_logins": failed_logins,
        "otp_failures": otp_failures,
        "suspicious_logins": suspicious_logins,
        "events_by_type": list(events_by_type),
        "events_over_time": list(events_over_time),
        "top_ips": list(top_ips),
    }

    return render(request, "fraud/dashboard.html", context)
