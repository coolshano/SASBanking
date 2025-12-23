from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone

#class Profile(models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    #phone = models.CharField(max_length=20, blank=True)

    #def __str__(self):
    #    return self.user.username

# Optional: automatically create Profile when User is created
#@receiver(post_save, sender=User)
#def create_user_profile(sender, instance, created, **kwargs):
    #if created:
        #Profile.objects.create(user=instance)


User = settings.AUTH_USER_MODEL


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.email
    

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class LoginOTP(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=5)

    def __str__(self):
        return f"OTP for {self.user.email}"