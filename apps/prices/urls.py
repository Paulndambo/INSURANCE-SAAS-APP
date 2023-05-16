from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.prices.views import PricingPlanViewSet, BulkPricingPlanUploadAPIView, PricingPlanCoverMappingViewSet

router = DefaultRouter()
router.register("pricing-plans", PricingPlanViewSet, basename="pricing-plans")
router.register("pricing-plan-cover-mappings", PricingPlanCoverMappingViewSet, basename="pricing-plan-cover-mappings"),

urlpatterns = [
    path("", include(router.urls)),
    path(
        "pricing-plan-bulk-upload/",
        BulkPricingPlanUploadAPIView.as_view(),
        name="pricing-plan-bulk-upload",
    ),
]
