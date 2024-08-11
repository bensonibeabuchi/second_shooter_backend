from django.urls import path, include, re_path
from .views import *


urlpatterns = [
    re_path(
        r'^o/(?P<provider>\S+)/$',
        CustomProviderAuthView.as_view(),
        name='provider-auth'
    ),
    path('register/', CustomUserCreateView.as_view(), name='create-user'),
    path('activate/', CustomActivationView.as_view(), name='activate'),
    path('resend-otp/', ResendOTPView.as_view(), name='send-otp'),
    path('login/', CustomTokenObtainPairView.as_view()),
    path('user/profile/', UserProfileView.as_view(), name='user-profile'),
    path('jwt/refresh/', CustomTokenRefreshView.as_view()),
    path('jwt/verify/', CustomTokenVerifyView.as_view()),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path('logout/', LogoutView.as_view()),
    # path('', include('djoser.urls.jwt')),
    # path('', include('djoser.social.urls')),
    # path('', include('djoser.urls')),
]