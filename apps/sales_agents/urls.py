from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.sales_agents.views import (SalesAgentPolicyViewSet,
                                     SalesAgentSchemeGroupViewSet)

router = DefaultRouter()
router.register("policies", SalesAgentPolicyViewSet, basename="policies")
router.register("scheme-groups", SalesAgentSchemeGroupViewSet, basename="scheme-groups")

urlpatterns = [
    path("", include(router.urls)),
]