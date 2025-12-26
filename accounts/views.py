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
from fraud.models import FraudEvent
from fraud.services import detect_login_fraud,  detect_otp_fraud, detect_geo_anomaly
from fraud.utils import get_client_ip, get_geo_location
from django.shortcuts import render, redirect


@login_required #User Dashboard login
def dashboard(request):
    return render(request, 'accounts/index.html')

#User Registration
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

#OTP view 
# def otp_view(request):
#     otp = request.session.get("otp")
#     user_id = request.session.get("otp_user_id")

#     if not otp or not user_id:
#         return redirect("login")

#     if request.method == "POST":
#         entered_otp = request.POST.get("otp")

#         if entered_otp == otp:
#             user = User.objects.get(id=user_id)
#             login(request, user)


#             request.session.pop("otp", None)
#             request.session.pop("otp_user_id", None)

#             if user.email == "managersasbanking@gmail.com":
#                 return redirect("users_dashboard")

#             return redirect("dashboard")

#         return render(request, 'accounts/otp.html', {"error": "Invalid OTP"})

#     return render(request, 'accounts/otp.html')


def otp_view(request):
    otp = request.session.get("otp")
    user_id = request.session.get("otp_user_id")
    ip = get_client_ip(request)

    if not otp or not user_id:
        return redirect("login")

    user = User.objects.get(id=user_id)

    if request.method == "POST":
        entered_otp = request.POST.get("otp")

        # ----------------------------
        # INVALID OTP → FRAUD LOG
        # ----------------------------
        if entered_otp != otp:
            FraudEvent.objects.create(
                user=user,
                event_type="OTP_FAILURE",
                risk_score=25,
                ip_address=ip
            )

            risk = detect_otp_fraud(user, ip)
            if risk >= 70:
                return render(request, 'accounts/otp.html', {
                    "error": "Too many invalid OTP attempts. Please try again later."
                })

            return render(request, 'accounts/otp.html', {
                "error": "Invalid OTP"
            })

        # ----------------------------
        # VALID OTP → LOGIN
        # ----------------------------
        login(request, user)

        request.session.pop("otp", None)
        request.session.pop("otp_user_id", None)

        # ----------------------------
        # ROLE-BASED REDIRECT
        # ----------------------------
        if user.email == "managersasbanking@gmail.com":
            return redirect("users_dashboard")

        return redirect("dashboard")

    return render(request, 'accounts/otp.html')



#Login into the system
# def login_view(request):
#     if request.method == "POST":
#         email = request.POST.get("email")
#         password = request.POST.get("password")

#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             return render(request, 'accounts/login.html', {"error": "User not found"})

#         user = authenticate(username=user.username, password=password)
#         if not user:
#             return render(request, 'accounts/login.html', {"error": "Invalid credentials"})

#         otp = random.randint(100000, 999999)

#         request.session["otp"] = str(otp)
#         request.session["otp_user_id"] = user.id

#         send_mail(
#             "Your Login OTP",
#             f"Your OTP is {otp}",
#             settings.DEFAULT_FROM_EMAIL,
#             [email],
#         )

#         return redirect("otp")

#     return render(request, 'accounts/login.html')

# def login_view(request):
#     if request.method == "POST":
#         email = request.POST.get("email")
#         password = request.POST.get("password")
#         ip = get_client_ip(request)

#         # ----------------------------
#         # USER LOOKUP
#         # ----------------------------
#         try:
#             user_obj = User.objects.get(email=email)
#         except User.DoesNotExist:
#             FraudEvent.objects.create(
#                 user=None,
#                 event_type="FAILED_LOGIN",
#                 risk_score=20,
#                 ip_address=ip,
#                 metadata={"email": email}
#             )
#             return render(request, 'accounts/login.html', {
#                 "error": "User not found"
#             })

#         # ----------------------------
#         # AUTHENTICATION
#         # ----------------------------
#         user = authenticate(username=user_obj.username, password=password)
#         if not user:
#             FraudEvent.objects.create(
#                 user=user_obj,
#                 event_type="FAILED_LOGIN",
#                 risk_score=30,
#                 ip_address=ip
#             )
#             return render(request, 'accounts/login.html', {
#                 "error": "Invalid credentials"
#             })

#         # ----------------------------
#         # FRAUD CHECK BEFORE OTP
#         # ----------------------------
#         risk_score = detect_login_fraud(user, ip)

#         if risk_score >= 70:
#             FraudEvent.objects.create(
#                 user=user,
#                 event_type="SUSPICIOUS_LOGIN",
#                 risk_score=risk_score,
#                 ip_address=ip
#             )
#             return render(request, 'accounts/login.html', {
#                 "error": "Suspicious activity detected. Please try again later."
#             })

#         # ----------------------------
#         # OTP GENERATION
#         # ----------------------------
#         otp = random.randint(100000, 999999)

#         request.session["otp"] = str(otp)
#         request.session["otp_user_id"] = user.id

#         send_mail(
#             subject="Your Login OTP",
#             message=f"Your OTP is {otp}",
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             recipient_list=[email],
#         )

#         return redirect("otp")

#     return render(request, 'accounts/login.html')

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        ip = get_client_ip(request)
        location = get_geo_location(ip)

        # ----------------------------
        # USER LOOKUP
        # ----------------------------
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            FraudEvent.objects.create(
                user=None,
                event_type="FAILED_LOGIN",
                risk_score=20,
                ip_address=ip,
                metadata={"email": email, "location": location}
            )
            return render(request, 'accounts/login.html', {
                "error": "User not found"
            })

        # ----------------------------
        # AUTHENTICATION
        # ----------------------------
        user = authenticate(username=user_obj.username, password=password)
        if not user:
            FraudEvent.objects.create(
                user=user_obj,
                event_type="FAILED_LOGIN",
                risk_score=30,
                ip_address=ip,
                metadata={"location": location}
            )
            return render(request, 'accounts/login.html', {
                "error": "Invalid credentials"
            })

        # ----------------------------
        # FRAUD CHECKS
        # ----------------------------
        login_risk = detect_login_fraud(user, ip)
        geo_risk = detect_geo_anomaly(user, location)

        total_risk = login_risk + geo_risk

        if total_risk >= 80:
            FraudEvent.objects.create(
                user=user,
                event_type="SUSPICIOUS_LOGIN",
                risk_score=total_risk,
                ip_address=ip,
                metadata={"location": location}
            )
            return render(request, 'accounts/login.html', {
                "error": "Login blocked due to suspicious location change."
            })

        # ----------------------------
        # OTP GENERATION
        # ----------------------------
        otp = random.randint(100000, 999999)

        request.session["otp"] = str(otp)
        request.session["otp_user_id"] = user.id

        send_mail(
            subject="Your Login OTP",
            message=f"Your OTP is {otp}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )

        return redirect("otp")

    return render(request, 'accounts/login.html')


#Manager Dashboard
@login_required
def users_dashboard(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'accounts/users_dashboard.html', {
        'users': users
    })
