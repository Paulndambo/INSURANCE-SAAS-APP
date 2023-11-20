from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.reports.views import (GeneralAnalyticsAPIView,
                                MetabasePolicyHolderAPIView,
                                PolicyHolderReportViewSet)

router = DefaultRouter()
router.register("policy-holders-report", PolicyHolderReportViewSet, basename="policy-holders-report")


urlpatterns = [
    path("", include(router.urls)),
    path("metabase-policy-holders/", MetabasePolicyHolderAPIView.as_view(), name="metabase-policy-holders"),
    path("analytics/", GeneralAnalyticsAPIView.as_view(), name="analytics"),
]