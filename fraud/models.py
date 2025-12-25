from django.db import models
from django.contrib.auth.models import User

class FraudEvent(models.Model):
    EVENT_CHOICES = (
        ("FAILED_LOGIN", "Failed Login"),
        ("SUSPICIOUS_LOGIN", "Suspicious Login"),
        ("OTP_FAILURE", "OTP Failure"),
        ("HIGH_RISK_TRANSACTION", "High Risk Transaction"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    event_type = models.CharField(max_length=50, choices=EVENT_CHOICES)
    risk_score = models.IntegerField()
    ip_address = models.GenericIPAddressField()
    metadata = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event_type} | {self.user} | {self.risk_score}"
