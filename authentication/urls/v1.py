from django.urls import path , include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
#views
from authentication.views import *

urlpatterns = [
    path("register/",RegisterViewSet.as_view({"post":"create"})),
    path("verification/",RegisterViewSet.as_view({"post":"verify"})),
    path("resend-otp/",RegisterViewSet.as_view({"post":"resend"})),
    path("login/",LoginView.as_view()),
    path("password-reset-request/", PasswordResetRequestView.as_view(), name="password-reset-request"),
    path("password-reset-verify/", PasswordResetVerifyOTPView.as_view(), name="password-reset-verify"),
    path("password-reset/", PasswordResetView.as_view(), name="password-reset"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("profile/", UserProfileView.as_view(), name="user-profile"),
]