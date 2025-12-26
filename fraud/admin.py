from django.contrib import admin
from .models import FraudEvent

# @admin.register(FraudEvent)
# class FraudEventAdmin(admin.ModelAdmin):
#     list_display = (
#         "user",
#         "event_type",
#         "risk_score",
#         "ip_address",
#         "created_at"
#     )
#     list_filter = ("event_type", "risk_score", "created_at")
#     search_fields = ("user__username", "ip_address")
#     ordering = ("-created_at",)


@admin.register(FraudEvent)
class FraudEventAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "event_type",
        "risk_score",
        "ip_address",
        "country",
        "city",
        "created_at",
    )

    def country(self, obj):
        metadata = obj.metadata or {}
        location = metadata.get("location") or {}
        return location.get("country", "-")

    def city(self, obj):
        metadata = obj.metadata or {}
        location = metadata.get("location") or {}
        return location.get("city", "-")

    country.short_description = "Country"
    city.short_description = "City"