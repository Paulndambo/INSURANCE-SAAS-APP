from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.policies.views import (
    PolicyModelViewSet,
    PolicyCancellationViewSet,
    PolicyStatusUpdateViewSet,
)

router = DefaultRouter()
router.register("", PolicyModelViewSet, basename="policies")
router.register(
    "policy-cancellations", PolicyCancellationViewSet, basename="policy-cancellations"
)
router.register(
    "policy-status-updates", PolicyStatusUpdateViewSet, basename="policy-status-updates"
)

urlpatterns = [
    path("", include(router.urls)),
]
