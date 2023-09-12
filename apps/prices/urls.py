from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.prices.medical.views import GeneralMedicalCoverAPIView
from apps.prices.views import (BulkPricingPlanUploadAPIView,
                               DependentPricingAPIView,
                               ExtendedCoverLevelsAPIView,
                               ExtendedDependentPricingAPIView,
                               MainMemberPricingAPIView, ObligationViewSet,
                               PricingPlanAPIView,
                               PricingPlanCoverMappingAPIView,
                               PricingPlanExtendedPremiumMappingAPIView,
                               PricingPlanViewSet)

router = DefaultRouter()
router.register("pricing-plans", PricingPlanViewSet, basename="pricing-plans")
router.register("obligations", ObligationViewSet, basename="obligations")
#router.register("pricing-plan-api", PricingPlanAPIView, basename="pricing-plan-api")


urlpatterns = [
    path("", include(router.urls)),
    path("pricing-plan-bulk-upload/", BulkPricingPlanUploadAPIView.as_view(), name="pricing-plan-bulk-upload"),
    path("dependent-pricing/", DependentPricingAPIView.as_view(), name="dependent-pricing"),
    path("pricing-plan-cover-mapping/", PricingPlanCoverMappingAPIView.as_view(), name="pricing-plan-cover-mapping"),
    path("extended-family-prices/", PricingPlanExtendedPremiumMappingAPIView.as_view(), name="extended-family-prices"),
    path("extended-family-pricing/", ExtendedDependentPricingAPIView.as_view(), name="extended-family-pricing"),
    path("extended-family-cover-levels/", ExtendedCoverLevelsAPIView.as_view(), name="extended-family-cover-levels"),
    path("main-member-pricing/", MainMemberPricingAPIView.as_view(), name="main-member-pricing"),
    path("pricing-plan-api/", PricingPlanAPIView.as_view(), name="pricing-plan-api"),
    path("general-medical-plan-pricing/", GeneralMedicalCoverAPIView.as_view(), name="general-medical-plan-pricing"),
]
