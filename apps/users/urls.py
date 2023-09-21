from django.urls import include, path
from rest_framework_nested.routers import DefaultRouter

from . import views
from .views import *

router = DefaultRouter()
router.register("users", views.UserModelViewSet, basename="users")
router.register("memberships", views.MembershipViewSet, basename="memberships")
router.register("profiles", views.ProfileModelViewSet, basename="profiles")
router.register("policyholders", views.PolicyHolderViewSet, basename="policy-holders")
router.register("policyholder-relatives", views.PolicyHolderRelativeViewSet, basename="policyholder-relatives",)


urlpatterns = [
    # path('', views.getRoutes),
    path("forgot-password/", views.ForgotPasswordAPIView.as_view(), name="forgot_password",),
    path("change-password/<str:token>/", views.ChangePasswordAPIView.as_view(), name="change_password",),
    path("login/", GetAuthToken.as_view(), name="login"),
    path("register/", RegisterAPI.as_view(), name="register"),
    path("", include(router.urls)),
    path("bulk-relatives-upload/", BulkPolicyHolderRelativeAPIView.as_view(), name="bulk-relatives-upload"),
]
