from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.payments.mpesa.views import (LipaNaMpesaAPIView,
                                       LipaNaMpesaCallbackAPIView)
from apps.payments.views import (BankStatementAPIView,
                                 BankStatementPaymentAPIView,
                                 ManualPolicyPaymentAPIView,
                                 PolicyPremiumViewSet)

router = DefaultRouter()
router.register("premiums", PolicyPremiumViewSet, basename="premiums")

urlpatterns = [
    path("", include(router.urls)),
    path("manual-payment/", ManualPolicyPaymentAPIView.as_view(), name="manual-payment"),
    path("load-bank-statement/", BankStatementPaymentAPIView.as_view(), name="load-bank-statement"),
    path("bank-statements/", BankStatementAPIView.as_view(), name="bank-statements"),
    path("lipa-na-mpesa/", LipaNaMpesaAPIView.as_view(), name="lipa-na-mpesa"),
    path("lipa-na-mpesa-callback/", LipaNaMpesaCallbackAPIView.as_view(), name="lipa-na-mpesa-callback"),
]