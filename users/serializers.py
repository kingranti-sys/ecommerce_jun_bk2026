from django.conf import settings

from datetime import timedelta
import secrets

from django.contrib.auth import authenticate
# from django.utils import timezone
# from django.template.loader import render_to_string
# from django.core.mail import EmailMultiAlternatives
# import resend
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, EmailVerification

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style=["input_type", "password"])

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "password"
        ]

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            is_active=True,
        )    

        '''
        otp = str(secrets.randbelow(900000) + 100000)

        EmailVerification.objects.create(
            user=user,
            otp=otp,
            expires_at=timezone.now() + timedelta(minutes=10)
        )   

        html_message = render_to_string(
            "verification_email.html",
            {
                "otp": otp,
                "user": user,
            }
        )
        '''
        # resend.Emails.send({
        #     "from": settings.DEFAULT_FROM_EMAIL,
        #     "to": [user.email],
        #     "subject": "verify your email",
        #     "html": html_message,
        # })
        '''
        email = EmailMultiAlternatives(
           subject="verify your email",
            body="",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email]
        ) 

        email.attach_alternative(html_message, "text/html")

        email.send(fail_silently=False)
        '''
        return user


class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            email = email,
            password = password
        )

        if not user:
            raise serializers.ValidationError("Invalid email or password")

        if not user.is_active:
            raise serializers.ValidationError("Please verify your email first")

        attrs["user"] = user

        return attrs

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except Exception:
            raise serializers.ValidationError("Invalid or expired refresh token.")