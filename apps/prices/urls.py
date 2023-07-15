from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.prices.views import (
    PricingPlanViewSet, 
    BulkPricingPlanUploadAPIView, 
    PricingPlanCoverMappingAPIView,
    DependentPricingAPIView,
    PricingPlanExtendedPremiumMappingAPIView,
    ExtendedDependentPricingAPIView,
    ExtendedCoverLevelsAPIView,
    MainMemberPricingAPIView,
    PricingPlanAPIView
)

router = DefaultRouter()
router.register("pricing-plans", PricingPlanViewSet, basename="pricing-plans")
router.register("pricing-plan-api", PricingPlanAPIView, basename="pricing-plan-api")


urlpatterns = [
    path("", include(router.urls)),
    path("pricing-plan-bulk-upload/", BulkPricingPlanUploadAPIView.as_view(), name="pricing-plan-bulk-upload"),
    path("dependent-pricing/", DependentPricingAPIView.as_view(), name="dependent-pricing"),
    path("pricing-plan-cover-mapping/", PricingPlanCoverMappingAPIView.as_view(), name="pricing-plan-cover-mapping"),
    path("extended-family-prices/", PricingPlanExtendedPremiumMappingAPIView.as_view(), name="extended-family-prices"),
    path("extended-family-pricing/", ExtendedDependentPricingAPIView.as_view(), name="extended-family-pricing"),
    path("extended-family-cover-levels/", ExtendedCoverLevelsAPIView.as_view(), name="extended-family-cover-levels"),
    path("main-member-pricing/", MainMemberPricingAPIView.as_view(), name="main-member-pricing"),
    #path("pricing-plan-api/", PricingPlanAPIView.as_view(), name="pricing-plan-api"),
]
