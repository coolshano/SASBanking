from django.contrib import admin
from .models import LoginOTP, Profile

@admin.register(LoginOTP)
class LoginOTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'otp', 'is_used', 'created_at')
    list_filter = ('is_used', 'created_at')
    search_fields = ('user__email',)
    ordering = ('-created_at',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')
