from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.payments.views import (
    PolicyPremiumViewSet,
    ManualPolicyPaymentAPIView,
    BankStatementPaymentAPIView,
    BankStatementAPIView
)

router = DefaultRouter()
router.register("premiums", PolicyPremiumViewSet, basename="premiums")

urlpatterns = [
    path("", include(router.urls)),
    path("manual-payment/", ManualPolicyPaymentAPIView.as_view(), name="manual-payment"),
    path("load-bank-statement/", BankStatementPaymentAPIView.as_view(), name="load-bank-statement"),
    path("bank-statements/", BankStatementAPIView.as_view(), name="bank-statements"),
]