from django.shortcuts import render
import secrets
from datetime import timedelta
from django.conf import settings

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

# import resend

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from .models import User, EmailVerification
from .serializers import RegisterSerializer, VerifyEmailSerializer, ResendOTPSerializer, LoginSerializer, LogoutSerializer


class RegisterView(APIView):

  def post(self, request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
      serializer.save()

      return Response({"message": "Registeration successful."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):

  def post(self, request):
    serializer = VerifyEmailSerializer(data=request.data)

    if not serializer.is_valid():
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    email = serializer.validated_data["email"]
    otp = serializer.validated_data["otp"]

    try:
      user = User.objects.get(email=email)
    except User.DoesNotExist:
      return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    try:
      verification = EmailVerification.objects.get(user=user)
    except EmailVerification.DoesNotExist:
      return Response({"error": "Verification record not found"}, status=status.HTTP_404_NOT_FOUND)

    if verification.otp != otp:
      return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

    if timezone.now() > verification.expires_at:
      return Response({"error": "OTP has expired."}, status=status.HTTP_400_BAD_REQUEST)

    user.is_active = True
    user.save()

    verification.delete()

    return Response({"message": "Email verified successfully"}, status=status.HTTP_200_OK)


class ResendOTPView(APIView):

  def post(self, request):
    serializer = ResendOTPSerializer(data=request.data)

    if not serializer.is_valid():
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    email = serializer.validated_data["email"]

    try:
      user = User.objects.get(email=email)
    except User.DoesNotExist:
      return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    if user.is_active:
      return Response({"message": "Email is already verified"}, status=status.HTTP_400_BAD_REQUEST)

    try:
      verification = EmailVerification.objects.get(user=user)
    except EmailVerification.DoesNotExist:
      return Response({"error": "Verification record not found"}, status=status.HTTP_404_NOT_FOUND)

    new_otp = str(secrets.randbelow(900000) + 100000)

    verification.otp = new_otp
    verification.expires_at = timezone.now() + timedelta(minutes=10)
    verification.save()

    html_message = render_to_string(
      "verification_email.html",
      {
        "user": user,
        "otp": new_otp, 
      }
    )

    '''
    try:
      resend.Emails.send({
        "from": settings.DEFAULT_FROM_EMAIL,
        "to": [user.email],
        "subject": "Your new verification code",
        "html": html_message,
      })
    except Exception as e:
      print("RESEND OTP ERROR:", repr(e))
      raise
    '''

    
    new_email = EmailMultiAlternatives(
      subject="You new verification code",
      body=f"Your new verification code is {new_otp}",
      from_email=settings.DEFAULT_FROM_EMAIL,
      to=[user.email],
    )

    new_email.attach_alternative(html_message, "text/html")
    new_email.send()

    return Response(
      {"message": "A new verification code has been sent to your email."}, 
      status=status.HTTP_200_OK
    )


class LoginView(APIView):

  def post(self, request):
    serializer = LoginSerializer(data=request.data)

    if not serializer.is_valid():
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = serializer.validated_data["user"]

    refresh = RefreshToken.for_user(user)

    return Response({
      "refresh": str(refresh),
      "access": str(refresh.access_token)
    }) 


class ProfileView(APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request):
    return Response({
      "message": "You are authenticated",
      "user": request.user.email,
    })

class LogoutView(APIView):
  permission_classes = [IsAuthenticated]

  def post(self, request):

    serializer = LogoutSerializer(data=request.data)

    if not serializer.is_valid():
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer.save()

    return Response({'message': "Successfully logged out"}, status=status.HTTP_200_OK)