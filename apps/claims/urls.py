from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.claims.views import ClaimDocumentModelViewSet, ClaimModelViewSet, ClaimStatusUpdatesModelViewSet

router = DefaultRouter()
router.register("", ClaimModelViewSet, basename="claims")
router.register("claim-documents", ClaimDocumentModelViewSet, basename="claim-documents")
router.register("claim-status-updates", ClaimStatusUpdatesModelViewSet, basename="claim-status-updates")

urlpatterns = [
    path("", include(router.urls)),
]