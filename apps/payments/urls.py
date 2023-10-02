from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.payments.mpesa.views import (LipaNaMpesaAPIView,
                                       LipaNaMpesaCallbackAPIView,
                                       LipaPremiumNaMpesaAPIView)
from apps.payments.views import (BankStatementAPIView,
                                 BankStatementPaymentAPIView,
                                 DynamicManualPaymentsAPIView,
                                 ManualPolicyPaymentAPIView,
                                 PolicyPremiumViewSet)

router = DefaultRouter()
router.register("premiums", PolicyPremiumViewSet, basename="premiums")

urlpatterns = [
    path("", include(router.urls)),
    path("manual-payment/", ManualPolicyPaymentAPIView.as_view(), name="manual-payment"),
    path("multiple-manual-payments/", DynamicManualPaymentsAPIView.as_view(), name="multiple-manual-payments"),
    path("load-bank-statement/", BankStatementPaymentAPIView.as_view(), name="load-bank-statement"),
    path("bank-statements/", BankStatementAPIView.as_view(), name="bank-statements"),
    path("lipa-na-mpesa/", LipaNaMpesaAPIView.as_view(), name="lipa-na-mpesa"),
    path("lipa-premium/", LipaPremiumNaMpesaAPIView.as_view(), name="lipa-premium"),
    path("lipa-na-mpesa-callback/", LipaNaMpesaCallbackAPIView.as_view(), name="lipa-na-mpesa-callback"),
]