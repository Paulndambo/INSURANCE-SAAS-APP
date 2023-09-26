from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.customer.policies.views import CustomerPolicyViewSet

router = DefaultRouter()
router.register("policies", CustomerPolicyViewSet, basename="policies")

urlpatterns = [
    path("", include(router.urls)),
]