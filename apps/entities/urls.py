from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.entities.views import BrokerViewSet, SalesAgentViewSet

router = DefaultRouter()
router.register("brokers", BrokerViewSet, basename="brokers")
router.register("sales-agents", SalesAgentViewSet, basename="sales-agents")

urlpatterns = [
    path("", include(router.urls)),
]