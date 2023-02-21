from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.claims.views import (
    ClaimDocumentModelViewSet,
    ClaimModelViewSet,
    ClaimStatusUpdatesModelViewSet,
    ClaimAdditionalInfoModelViewSet,
)

router = DefaultRouter()
router.register("", ClaimModelViewSet, basename="claims")
router.register(
    "claim-documents", ClaimDocumentModelViewSet, basename="claim-documents"
)
router.register(
    "claim-status-updates",
    ClaimStatusUpdatesModelViewSet,
    basename="claim-status-updates",
)
router.register(
    "claim-additional-info",
    ClaimAdditionalInfoModelViewSet,
    basename="claim-additional-info",
)

urlpatterns = [
    path("", include(router.urls)),
]
