from django.conf import settings
from rest_framework import generics, serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.payments.models import MpesaTransaction, PaymentLog, PolicyPremium
from apps.payments.mpesa.mpesa_callback_data import \
    mpesa_callback_data_distructure
from apps.payments.mpesa.utils import MpesaGateWay
from apps.payments.serializers import (LipaNaMpesaCallbackSerializer,
                                       LipaNaMpesaSerializer)
from apps.users.models import Profile

BASE_BACKEND_URL = "https://eager-close-hen.ngrok-free.app"

class LipaNaMpesaCallbackAPIView(generics.CreateAPIView):
    serializer_class = LipaNaMpesaCallbackSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data

        print(f"Mpesa Data: {data}")
        membership = request.query_params.get("membership")
        id_number = request.query_params.get("id_number")

        print(f"ID Number: {id_number}, Membership ID: {membership}")

        #return Response({"message": "Hello World"})
        serializer = self.serializer_class(data=data)
        
        if serializer.is_valid(raise_exception=True):

            callback_data = mpesa_callback_data_distructure(data)
            mpesa_transaction = MpesaTransaction.objects.create(**callback_data)
            if membership and id_number:
                mpesa_transaction.id_number = id_number
                mpesa_transaction.membership_id = membership
            elif membership:
                mpesa_transaction.membership_id = membership
            elif membership and id_number:
                mpesa_transaction.id_number = id_number
            mpesa_transaction.save()

            print(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LipaPremiumNaMpesaAPIView(generics.CreateAPIView):
    serializer_class = LipaNaMpesaSerializer

    def post(self, request):
        data = request.data
        
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):  
            premium = serializer.validated_data.get("premium")
            id_number = serializer.validated_data.get("id_number")
            amount = serializer.validated_data.get("amount")
            phone_number = serializer.validated_data.get("phone_number")

            membership_premium = None
            premium_amount = int(amount)
            callback_url = f"{BASE_BACKEND_URL}/payments/lipa-na-mpesa-callback/?id_number={id_number}"

            if id_number and premium:
                membership_premium = PolicyPremium.objects.filter(id=premium).first()
                premium_amount = int(membership_premium.expected_payment)
                callback_url = f"{BASE_BACKEND_URL}/payments/lipa-na-mpesa-callback/?membership={membership_premium.membership.id}&id_number={id_number}/"

            elif premium:
                membership_premium = PolicyPremium.objects.filter(id=premium).first()
                premium_amount = int(membership_premium.expected_payment)
                callback_url = f"{BASE_BACKEND_URL}/payments/lipa-na-mpesa-callback/?membership={membership_premium.membership.id}&id_number={id_number}/"

            elif id_number:
                profile = Profile.objects.filter(id_number=id_number).first()
                if profile:
                    membership_premium = PolicyPremium.objects.filter(membership__user=profile.user).order_by("-expected_date").first()
                    premium_amount = int(membership_premium.expected_payment)
                    callback_url = f"{BASE_BACKEND_URL}/payments/lipa-na-mpesa-callback/?membership={membership_premium.membership.id}&id_number={id_number}/"
                

            payment_object = {
                "callback_url": callback_url,
                "id_number": id_number,
                "premium": premium
            }
            print(payment_object)

            mpesa = MpesaGateWay()
            mpesa.stk_push(
                phone_number=phone_number,
                amount=premium_amount,
                callback_url=callback_url,
                account_reference="SmartSure Premium Payment",
                transaction_desc="This is a premium payment using mpesa transaction"
            )
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
                callback_url="https://dea1-105-163-158-150.ngrok-free.app/payments/lipa-na-mpesa-callback/",
                account_reference="SmartSure Premium Payment",
                transaction_desc="This is a premium payment using mpesa transaction"
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  