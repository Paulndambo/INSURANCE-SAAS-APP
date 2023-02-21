from rest_framework.routers import DefaultRouter
from django.urls import path, include
from apps.dependents.views import DependentModelViewSet, BeneficiaryModelViewSet

router = DefaultRouter()
router.register("dependents", DependentModelViewSet, basename="dependents")
router.register("beneficiaries", BeneficiaryModelViewSet, basename="beneficiaries")


urlpatterns = [
    path("", include(router.urls)),
]
