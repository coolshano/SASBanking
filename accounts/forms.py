from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=True, max_length=20)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'phone']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Save phone in profile
            user.profile.phone = self.cleaned_data['phone']
            user.profile.save()
        return user