from django.urls import path, include
from apps.sales.views import (
    TemporaryDataHoldingAPIView,
    TemporaryCancelledMemberDataAPIView,
    TemporaryDependentDataAPIView,
    TemporaryNewMemberDataAPIView,
    TemporaryPaidMemberDataAPIView,
    GenerateGWPReportAPIView,
    PricingPlanSchemeMappingAPIView
)

urlpatterns = [
    path(
        "new-members-upload/",
        TemporaryNewMemberDataAPIView.as_view(),
        name="new-members-upload",
    ),
    path("pricing-plan-scheme-mapping/", PricingPlanSchemeMappingAPIView.as_view(),
        name="pricing-plan-scheme-mapping"),
    path(
        "paid-members-upload/",
        TemporaryPaidMemberDataAPIView.as_view(),
        name="paid-members-upload",
    ),
    path(
        "dependents-and-beneficiaries-upload/",
        TemporaryDependentDataAPIView.as_view(),
        name="dependents-and-beneficiaries-upload",
    ),
    path(
        "cancelled-members-upload/",
        TemporaryCancelledMemberDataAPIView.as_view(),
        name="cancelled-members-upload",
    ),
    path(
        "bulk-data-upload/",
        TemporaryDataHoldingAPIView.as_view(),
        name="bulk-data-upload",
    ),
    path(
        "generate-gwp-report/",
        GenerateGWPReportAPIView.as_view(),
        name="generate-gwp-report",
    ),
]
