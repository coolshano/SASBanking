from django.contrib import admin
from .models import FraudEvent

@admin.register(FraudEvent)
class FraudEventAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "event_type",
        "risk_score",
        "ip_address",
        "created_at"
    )
    list_filter = ("event_type", "risk_score", "created_at")
    search_fields = ("user__username", "ip_address")
    ordering = ("-created_at",)