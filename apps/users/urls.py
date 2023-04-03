from django.urls import path
from . import views
from django.urls import path, include
from rest_framework_nested.routers import DefaultRouter

from .views import *


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = DefaultRouter()
router.register("users", views.UserModelViewSet, basename="users")
router.register("memberships", views.MembershipViewSet, basename="memberships")
router.register("profiles", views.ProfileModelViewSet, basename="profiles")
router.register("policyholders", views.PolicyHolderViewSet, basename="policy-holders")
router.register(
    "policyholder-relatives",
    views.PolicyHolderViewSet,
    basename="policyholder-relatives",
)


urlpatterns = [
    # path('', views.getRoutes),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "forgot-password/",
        views.ForgotPasswordAPIView.as_view(),
        name="forgot_password",
    ),
    path(
        "change-password/<str:token>/",
        views.ChangePasswordAPIView.as_view(),
        name="change_password",
    ),
    path("", include(router.urls)),
]
