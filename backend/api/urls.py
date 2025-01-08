from django.urls import path
from api.views import RegisterView
from api.views import MytokenObtainPairView, PasswordResetEmailVerifyAPIView, PasswordChangeAPIView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("user/register/", RegisterView.as_view(), name="register"),
    path("user/token/", MytokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("user/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("user/password-reset/<str:email>/", PasswordResetEmailVerifyAPIView.as_view(), name="password_reset_email_verify"),
    path("user/password-change/", PasswordChangeAPIView.as_view(), name="password_change"),
]