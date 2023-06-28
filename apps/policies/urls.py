from django.urls import path, include
#from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from apps.policies.views import (
    PolicyModelViewSet,
    PolicyCancellationViewSet,
    CycleModelViewSet,
    CycleStatusModelViewSet
    # PolicyStatusUpdatesViewSet,
)
from apps.dependents.views import DependentModelViewSet, BeneficiaryModelViewSet


router = routers.DefaultRouter()
router.register("policies", PolicyModelViewSet, basename="policies")
router.register(
    "policy-cancellations", PolicyCancellationViewSet, basename="policy-cancellations"
)
router.register("cycles", CycleModelViewSet, basename="cycles")
router.register("cycles-status-updates", CycleStatusModelViewSet, basename="cycles-status-updates")
# router.register("policy-status-updates", PolicyStatusUpdatesViewSet, basename="policy-status-updates")

policies_router = routers.NestedDefaultRouter(router, "policies", lookup="policy")
policies_router.register("dependents", DependentModelViewSet, basename="dependents")
policies_router.register("beneficiaries", BeneficiaryModelViewSet, basename="beneficiaries")


urlpatterns = [
    path("", include(router.urls)),
    path("", include(policies_router.urls)),
]
