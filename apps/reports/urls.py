from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.reports.views import (
    PolicyHolderReportViewSet
)

router = DefaultRouter()
router.register("policy-holders-report", PolicyHolderReportViewSet, basename="policy-holders-report")


urlpatterns = [
    path("", include(router.urls)),
]