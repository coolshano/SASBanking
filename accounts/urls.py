from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.views import LogoutView




urlpatterns = [
    path('register/', views.register, name='register'),
    ##path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path("login/", views.login_view, name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('otp/', views.otp_view, name='otp'),
    path('', views.dashboard, name='dashboard'),
    path('dashboard/users/', views.users_dashboard, name='users_dashboard'),

    #Password reset mechanism
    path("password-reset/", auth_views.PasswordResetView.as_view(
        template_name="accounts/password_reset.html"
    ), name="password_reset"),

    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(
        template_name="accounts/password_reset_done.html"
    ), name="password_reset_done"),

    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="accounts/password_reset_confirm.html"
    ), name="password_reset_confirm"),

    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(
        template_name="accounts/password_reset_complete.html"
    ), name="password_reset_complete"),

]
