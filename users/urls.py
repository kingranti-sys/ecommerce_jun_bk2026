from django.urls import path

from .views import RegisterView, VerifyEmailView, ResendOTPView, LoginView,LogoutView, ProfileView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns= [
    path("register/", RegisterView.as_view(), name="register"),
    path("verify-email/", VerifyEmailView.as_view(), name="verify-email"),
    path("resend-otp/", ResendOTPView.as_view(), name="resend-otp"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),

]