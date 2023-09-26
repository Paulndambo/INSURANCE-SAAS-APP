from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.sales_agents.views import SalesAgentPolicyViewSet

router = DefaultRouter()
router.register("policies", SalesAgentPolicyViewSet, basename="policies")

urlpatterns = [
    path("", include(router.urls)),
]