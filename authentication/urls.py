from django.urls import path,include 

from .views import (
    
    RegisterView,
    VerifyEmail,
    LoginAPIView,
    PasswordResetRequestAPIView,
    PasswordTokenCheckAPI,
    NewPasswordSettingViewAPI
    )
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('verify_email/',VerifyEmail.as_view(),name='verify_email'),
    path('refresh_token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/',LoginAPIView.as_view(),name='login'),
    path('password-reset-request/',PasswordResetRequestAPIView.as_view(),name='password-reset-request'),
    path('password-reset-check/<uidb64>/<token>/',PasswordTokenCheckAPI.as_view(),name='passord-reset-confirm'),
    path('password-reset-complete/',NewPasswordSettingViewAPI.as_view(),name='passord-reset-complete')

]
