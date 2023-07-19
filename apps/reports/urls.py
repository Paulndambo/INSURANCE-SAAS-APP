from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.reports.views import (
    PolicyHolderReportViewSet,
    MetabasePolicyHolderAPIView
)

router = DefaultRouter()
router.register("policy-holders-report", PolicyHolderReportViewSet, basename="policy-holders-report")


urlpatterns = [
    path("", include(router.urls)),
    path("metabase-policy-holders/", MetabasePolicyHolderAPIView.as_view(), name="metabase-policy-holders"),
]