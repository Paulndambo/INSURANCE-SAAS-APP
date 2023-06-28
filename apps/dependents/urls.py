from rest_framework.routers import DefaultRouter
from django.urls import path, include
from apps.dependents.views import (
    DependentModelViewSet, 
    BeneficiaryModelViewSet,
    FamilyMemberPricingViewSet
)

router = DefaultRouter()
router.register("dependents", DependentModelViewSet, basename="dependents")
router.register("beneficiaries", BeneficiaryModelViewSet, basename="beneficiaries")
router.register("family-member-pricing", FamilyMemberPricingViewSet, basename="family-member-pricing")


urlpatterns = [
    path("", include(router.urls)),
]
