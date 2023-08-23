from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.payments.views import PolicyPremiumViewSet

router = DefaultRouter()
router.register("premiums", PolicyPremiumViewSet, basename="premiums")

urlpatterns = [
    path("", include(router.urls)),
]