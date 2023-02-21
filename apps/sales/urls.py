from django.urls import path, include
from apps.sales.views import (
    TemporaryDataHoldingAPIView,
    TemporaryCancelledMemberDataAPIView,
    TemporaryDependentDataAPIView,
    TemporaryNewMemberDataAPIView,
    TemporaryPaidMemberDataAPIView,
)

urlpatterns = [
    path(
        "new-members-upload/",
        TemporaryNewMemberDataAPIView.as_view(),
        name="new-members-upload",
    ),
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
]
