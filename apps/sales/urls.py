from django.urls import path, include
from apps.sales.views import (
    OnboardingAPPAPIView,
    BulkTemporaryPaidMemberUploadAPIView,
    OnboardingInitiateAPIView,
    BulkTemporaryDependentUploadAPIView,
    BulkTemporaryCancelledMemberUploadAPIView,
    BulkTemporaryNewMemberUploadAPIView,
    TemporaryDataHoldingAPIView,
    FailedUploadDataAPIView,
    NewMembersAPIView,
    PolicyPurchaseAPIView,
    CreditLifePolicyPurchaseAPIView
)

urlpatterns = [
    path("", OnboardingAPPAPIView.as_view(), name="get-routes"),
    path("bulk-upload/initiate-onboarding/", OnboardingInitiateAPIView.as_view(), name="initiate-onboarding"),
    path("bulk-upload/paid-members/", BulkTemporaryPaidMemberUploadAPIView.as_view(), name="paid-members"),
    path("bulk-upload/cancelled-members/", BulkTemporaryCancelledMemberUploadAPIView.as_view(), name="cancelled-members"),
    path("bulk-upload/new-members/", BulkTemporaryNewMemberUploadAPIView.as_view(), name="new-members"),
    path("bulk-upload/family-members/", BulkTemporaryDependentUploadAPIView.as_view(), name="family-members"),
    path("bulk-upload/temporary-data-upload/", TemporaryDataHoldingAPIView.as_view(), name="temporary-data-upload"),
    path("bulk-upload/failed-uploads/", FailedUploadDataAPIView.as_view(), name="failed-uploads"),
    path("bulk-upload/bulk-new-members-list/", NewMembersAPIView.as_view(), name="bulk-new-members-list"),
    path("policy-purchase/", PolicyPurchaseAPIView.as_view(), name="policy-purchase"),
    path("credit-life-policy-purchase/", CreditLifePolicyPurchaseAPIView.as_view(), name="credit-life-policy-purchase"),
]
