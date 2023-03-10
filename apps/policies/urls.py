from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.policies.views import (
    PolicyModelViewSet,
    PolicyCancellationViewSet,
    CycleModelViewSet,
    CycleStatusModelViewSet
    # PolicyStatusUpdatesViewSet,
)

router = DefaultRouter()
router.register("policies", PolicyModelViewSet, basename="policies")
router.register(
    "policy-cancellations", PolicyCancellationViewSet, basename="policy-cancellations"
)
router.register("cycles", CycleModelViewSet, basename="cycles")
router.register("cycles-status-updates", CycleStatusModelViewSet, basename="cycles-status-updates")
# router.register("policy-status-updates", PolicyStatusUpdatesViewSet, basename="policy-status-updates")

urlpatterns = [
    path("", include(router.urls)),
]
