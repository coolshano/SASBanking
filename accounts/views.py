from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import RegisterForm
import random
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import LoginOTP
from django.http import HttpResponse
from django.middleware.csrf import get_token



@login_required #User Dashboard login
def dashboard(request):
    return render(request, 'accounts/index.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')   # ✅ redirect to login page
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def otp_view(request):
    otp = request.session.get("otp")
    user_id = request.session.get("otp_user_id")

    # 🚨 No OTP in session → go back to login
    if not otp or not user_id:
        return redirect("login")

    if request.method == "POST":
        entered_otp = request.POST.get("otp")

        if entered_otp == otp:
            user = User.objects.get(id=user_id)
            login(request, user)

            # ✅ SAFE cleanup (NO KeyError)
            request.session.pop("otp", None)
            request.session.pop("otp_user_id", None)

            return redirect("dashboard")

        return render(request, 'accounts/otp.html', {"error": "Invalid OTP"})

    return render(request, 'accounts/otp.html')


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'accounts/login.html', {"error": "User not found"})

        user = authenticate(username=user.username, password=password)
        if not user:
            return render(request, 'accounts/login.html', {"error": "Invalid credentials"})

        otp = random.randint(100000, 999999)

        request.session["otp"] = str(otp)
        request.session["otp_user_id"] = user.id

        send_mail(
            "Your Login OTP",
            f"Your OTP is {otp}",
            settings.DEFAULT_FROM_EMAIL,
            [email],
        )

        return redirect("otp")

    return render(request, 'accounts/login.html')
