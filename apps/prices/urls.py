from django.urls import path, include 
from rest_framework.routers import DefaultRouter
from apps.prices.views import PricingPlanViewSet

router = DefaultRouter()
router.register("pricing-plans", PricingPlanViewSet, basename="pricing-plans")

urlpatterns = [
    path("", include(router.urls)),
]