from django.urls import path
from .views import *

urlpatterns = [
    path('register/',AuthSignUpView.as_view()),
    path('login/',AuthLoginView.as_view()),
    path('change-password/',AuthChangePasswordView.as_view()),
    
    path('social-login/',SocialLoginView.as_view()),
    path('forgot-password/',ForgotPasswordView.as_view()),
    path('verify-otp/',VerifyOTPView.as_view()),
    path('reset-password/', ResetPasswordView.as_view()),

]
