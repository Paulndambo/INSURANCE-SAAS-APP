from django.conf import settings
from rest_framework import generics, serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.payments.models import MpesaTransaction
from apps.payments.mpesa.mpesa_callback_data import \
    mpesa_callback_data_distructure
from apps.payments.mpesa.utils import MpesaGateWay
from apps.payments.serializers import (LipaNaMpesaCallbackSerializer,
                                       LipaNaMpesaSerializer)

BASE_BACKEND_URL = settings.BASE_BACKEND_URL

class LipaNaMpesaCallbackAPIView(generics.CreateAPIView):
    serializer_class = LipaNaMpesaCallbackSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        
        if serializer.is_valid(raise_exception=True):

            callback_data = mpesa_callback_data_distructure(data)
            MpesaTransaction.objects.create(**callback_data)

            print(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LipaNaMpesaAPIView(generics.CreateAPIView):
    serializer_class = LipaNaMpesaSerializer

    def post(self, request):
        data = request.data

        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):  
            
            mpesa = MpesaGateWay()
            mpesa.stk_push(
                phone_number=data.get('phone_number'),
                amount=int(data.get("amount")),
                callback_url=f"{BASE_BACKEND_URL}/payments/lipa-na-mpesa-callback/",
                account_reference="SmartSure Premium Payment",
                transaction_desc="This is a premium payment using mpesa transaction"
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  