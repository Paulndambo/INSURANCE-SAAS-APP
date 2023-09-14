from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.core.views import InsurerViewSet

router = DefaultRouter()
router.register("insurers", InsurerViewSet, basename="insurers")

urlpatterns = [
    path("", include(router.urls)),
]