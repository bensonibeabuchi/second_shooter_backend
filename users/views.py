from django.conf import settings
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from djoser.social.views import ProviderAuthView
from .serializers import *
from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes
from rest_framework.permissions import AllowAny
from users.models import CustomUser
from django.conf import settings
from .serializers import *
from rest_framework import generics
import random
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.utils.translation import gettext_lazy as _
from django.utils.html import strip_tags
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes



from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

# GOOGLE LOGIN VIEW 
class CustomProviderAuthView(ProviderAuthView):
    @extend_schema(
        operation_id='Google/Facebook Authentication',
        description='This endpoint is used to Login with Google/Facebook',
        summary='This endpoint is used to Login with Google/Facebook',
        request= OpenApiTypes.OBJECT,
        responses={200: UserCreateSerializer},
    )
    def post(self, request, *args, **kwargs):
            response = super().post(request, *args, **kwargs)

            if response.status_code == 201:
                access_token = response.data.get('access')
                refresh_token = response.data.get('refresh')

                response.set_cookie(
                    'access',
                    access_token,
                    max_age=settings.AUTH_COOKIE_MAX_AGE,
                    path=settings.AUTH_COOKIE_PATH,
                    secure=settings.AUTH_COOKIE_SECURE,
                    httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                    samesite=settings.AUTH_COOKIE_SAMESITE
                )
                response.set_cookie(
                    'refresh',
                    refresh_token,
                    max_age=settings.AUTH_COOKIE_MAX_AGE,
                    path=settings.AUTH_COOKIE_PATH,
                    secure=settings.AUTH_COOKIE_SECURE,
                    httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                    samesite=settings.AUTH_COOKIE_SAMESITE
                )

            return response


# LOGIN VIEW 
class CustomTokenObtainPairView(TokenObtainPairView):
    @extend_schema(
        operation_id='Login with JWT Token',
        description='This endpoint is used to Login with with JWT Token',
        summary='This endpoint is used to Login with JWT Token. The Token is stored using http cookies automatically',
        request= OpenApiTypes.OBJECT,
        responses={200: UserCreateSerializer},
    )
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')

            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
            response.set_cookie(
                'refresh',
                refresh_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )

        return response


class CustomTokenRefreshView(TokenRefreshView):
    @extend_schema(
        operation_id='Refresh JWT Token',
        description='This endpoint refreshes the JWT Token',
        summary='This endpoint is used to refresh the JWT Token. The Token is then stored using HTTP cookies automatically',
        request=OpenApiTypes.OBJECT,
        responses={200: UserCreateSerializer},
    )
    def post(self, request, *args, **kwargs):
        # Get the refresh token from cookies
        refresh_token = request.COOKIES.get('refresh')

        # If the refresh token exists, add it to the request data
        if refresh_token:
            request.data['refresh'] = refresh_token

        # Call the original TokenRefreshView's post method
        response = super().post(request, *args, **kwargs)

        # If the response is successful, set the new access token in cookies
        if response.status_code == 200:
            access_token = response.data.get('access')
            if access_token:
                response.set_cookie(
                    'access',
                    access_token,
                    max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                    path=settings.AUTH_COOKIE_PATH,
                    secure=settings.AUTH_COOKIE_SECURE,
                    httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                    samesite=settings.AUTH_COOKIE_SAMESITE
                )

        return response


class CustomTokenVerifyView(TokenVerifyView):
    @extend_schema(
        operation_id='Verify JWT Token',
        description='This endpoint verifies the JWT Token',
        summary='This endpoint is used to verify the JWT Token. The Token is then stored using http cookies automatically',
        request= OpenApiTypes.OBJECT,
        responses={200: UserCreateSerializer},
    )

    def post(self, request, *args, **kwargs):
        # Get the access token from cookies
        access_token = request.COOKIES.get('access')

        # If the access token exists, add it to the request data
        if access_token:
            request.data['token'] = access_token

        # Call the original TokenVerifyView's post method
        return super().post(request, *args, **kwargs)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
 
    def post(self, request, *args, **kwargs):
        # Remove cookies from the browser
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('access')
        response.delete_cookie('refresh')
        return response
    


def generate_otp():
    return str(random.randint(100000, 999999))


class CustomUserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        operation_id='Create a User using OTP verification',
        description='This endpoint Create a User using OTP verification',
        summary='This endpoint is used to Create a User using OTP verification',
        request= OpenApiTypes.OBJECT,
        responses={200: CustomUserSerializer},
        )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save(is_active=False)
            otp = generate_otp()
            user.otp = otp
            user.save()

            email = user.email
            current_site = get_current_site(request)
            subject = 'Please Activate your account'
            html_message = render_to_string('users/activation.html', {
                'user': user,
                'domain': current_site.domain,
                'otp': otp,
                'site_name': settings.SITE_NAME,
            })
            from_email = 'bensonibeabuchistudios@gmail.com'
            plain_message = strip_tags(html_message)
            to_email = user.email
            email = EmailMultiAlternatives(subject, plain_message, from_email, [to_email])
            email.attach_alternative(html_message, "text/html")
            email.send()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomActivationView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
        operation_id='Activate user using OTP',
        description='This endpoint activates a user using OTP',
        summary='This endpoint is used to activate a user using the OTP sent to their email.',
        request= OpenApiTypes.OBJECT,
        responses={200: CustomUserSerializer},
        )
    
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        otp = request.data.get('otp')
        
        if not email or not otp:
            return Response({'error': _('Email and OTP are required.')}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': _('User does not exist.')}, status=status.HTTP_400_BAD_REQUEST)
        
        if user.otp == otp:
            user.is_active = True
            user.otp = None  # Clear the OTP after activation
            user.save()

            email = user.email
            current_site = get_current_site(self.request)
            subject = 'Account activated successufully'
            protocol = 'https' if self.request.is_secure() else 'http'
            html_message = render_to_string('users/confirmation.html', {
                'user': user,
                'domain': settings.DOMAIN,
                'protocol': protocol,
                'site_name': settings.SITE_NAME,
            })
            from_email = 'bensonibeabuchistudios@gmail.com'
            plain_message = strip_tags(html_message)
            to_email = user.email

            email = EmailMultiAlternatives(subject, plain_message, from_email, [to_email])
            email.attach_alternative(html_message, "text/html")
            email.send()

            return Response({'message': _('Account activated successfully')}, status=status.HTTP_200_OK)
        else:
            return Response({'error': _('Invalid OTP')}, status=status.HTTP_400_BAD_REQUEST)



class ResendOTPView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
        operation_id='Resend OTP to user',
        description='This endpoint resends OTP to user',
        summary='This endpoint is used to resend OTP to user provided they have their email address.',
        request= OpenApiTypes.OBJECT,
        responses={200: CustomUserSerializer},
        )

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')

        if not email:
            return Response({'error': _('Email is required.')}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': _('User does not exist.')}, status=status.HTTP_400_BAD_REQUEST)

        otp = generate_otp()
        user.otp = otp  # Save the OTP to the user model or another model
        user.save()

        email = user.email
        current_site = get_current_site(self.request)
        subject = 'Your new OTP'
        html_message = render_to_string('users/resendotp.html', {
                'user': user,
                'domain': current_site.domain,
                'otp': otp,
                'site_name': settings.SITE_NAME,
            })
        from_email = 'zlidementorled@gmail.com'
        plain_message = strip_tags(html_message)
        to_email = user.email

        email = EmailMultiAlternatives(subject, plain_message, from_email, [to_email])
        email.attach_alternative(html_message, "text/html")
        email.send()

        return Response({'message': _('OTP resent successfully.')}, status=status.HTTP_200_OK)
    

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        operation_id='Reset Password',
        description='This endpoint allows users to reset their password using the token sent to their email.',
        summary='Reset Password',
        request=ResetPasswordSerializer,
        responses={200: "Password reset successful."},
    )
    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            user = CustomUser.objects.get(email=serializer.validated_data['email'])
            email = user.email
            current_site = get_current_site(self.request)
            subject = 'Password changed successufully'
            protocol = 'https' if self.request.is_secure() else 'http'
            html_message = render_to_string('users/password_changed_confirmation.html', {
                'user': user,
                'domain': settings.DOMAIN,
                'protocol': protocol,
                'site_name': settings.SITE_NAME,
            })
            from_email = 'bensonibeabuchistudios@gmail.com'
            plain_message = strip_tags(html_message)
            to_email = user.email

            email = EmailMultiAlternatives(subject, plain_message, from_email, [to_email])
            email.attach_alternative(html_message, "text/html")
            email.send()


            return Response({'message': 'Password reset successful.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        operation_id='Forgot Password',
        description='This endpoint sends a password reset token to the user\'s email.',
        summary='Forgot Password',
        request=OpenApiTypes.OBJECT,
        responses={200: "Password reset email sent successfully."},
    )
    def post(self, request, *args, **kwargs):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = CustomUser.objects.get(email=serializer.validated_data['email'])
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            domain = settings.DOMAIN
            reset_link = f"{request.scheme}://{domain}/reset-password/{uid}/{token}/"

            subject = 'Reset Your Password'
            protocol = 'https' if self.request.is_secure() else 'http'
            html_message = render_to_string('users/password_reset.html', {
                'user': user,
                'reset_link': reset_link,
                'protocol': protocol,
                'domain': settings.DOMAIN,
                'site_name': settings.SITE_NAME,
            })
            from_email = 'bensonibeabuchistudios@gmail.com'
            plain_message = strip_tags(html_message)
            to_email = user.email

            email = EmailMultiAlternatives(subject, plain_message, from_email, [to_email])
            email.attach_alternative(html_message, "text/html")
            email.send()

            return Response({'message': 'Password reset email sent successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserSerializer

    def get_object(self):
        # This method is used to retrieve the object for the view, which will be the current user
        return self.request.user

    def get(self, request, *args, **kwargs):
        # Get the current logged-in user
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        # Update the current logged-in user's data
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        # Delete the current logged-in user
        user = self.get_object()
        user.delete()
        return Response(status=204)