from django.urls import path, include
#from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

## App Views
from apps.schemes.views import SchemeGroupModelViewSet, SchemeModelViewSet


## Other App Views
from apps.users.views import MembershipViewSet
from apps.dependents.views import DependentModelViewSet, BeneficiaryModelViewSet

router = routers.DefaultRouter()
router.register("schemes", SchemeModelViewSet, basename="schemes")
router.register("scheme-groups", SchemeGroupModelViewSet, basename="scheme-groups")

#router.register("memberships", MembershipViewSet, basename="memberships")

## Nested Routes
scheme_group_router = routers.NestedDefaultRouter(router, "scheme-groups", lookup="scheme_group")
scheme_group_router.register("memberships", MembershipViewSet, basename="membership")

membership_router = routers.NestedDefaultRouter(scheme_group_router, "memberships", lookup="membership")
membership_router.register("depedents", DependentModelViewSet, basename="dependents")
membership_router.register("beneficiaries", BeneficiaryModelViewSet, basename="beneficiaries")


urlpatterns = [
    path("", include(router.urls)),
    path("", include(scheme_group_router.urls)),
    path("", include(membership_router.urls)),
]
