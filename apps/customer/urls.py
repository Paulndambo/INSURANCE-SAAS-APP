from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.customer.policies.views import CustomerPolicyViewSet
from apps.customer.views import (CustomerBeneficiariesViewSet,
                                 CustomerDependentViewSet,
                                 CustomerExtendedDependentViewSet)

router = DefaultRouter()
router.register("policies", CustomerPolicyViewSet, basename="policies")
router.register("dependents", CustomerDependentViewSet, basename="depedents")
router.register("beneficiaries", CustomerBeneficiariesViewSet, basename="beneficiaries")
router.register("extended-dependents", CustomerExtendedDependentViewSet, basename="extended-dependents")

urlpatterns = [
    path("", include(router.urls)),
]