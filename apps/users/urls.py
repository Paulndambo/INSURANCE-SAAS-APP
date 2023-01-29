from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterAPI.as_view(), name='register'),
    path('forgot-password/', views.ForgotPasswordAPIView.as_view(), name='forgot_password'),
    path('change-password/<str:token>/', views.ChangePasswordAPIView.as_view(), name='change_password')
]
