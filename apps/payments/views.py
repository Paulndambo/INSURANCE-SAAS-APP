from django.shortcuts import render
import json

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework import generics, status
from rest_framework.response import Response

from apps.payments.models import (
    PolicyPremium,
    BankStatement,
    PolicyPayment
)
from apps.payments.serializers import (
    PolicyPremiumSerializer,
    ManualPolicyPaymentSerializer,
    BankStatementPaymentSerializer,
    BankStatementSerializer,
    PolicyPaymentSerializer
)

from apps.payments.payments_processor.manual_payment import ManualPaymentProcessingMixin
from apps.payments.payments_processor.bank_statement_payment import BankStatementPaymentProcessMixin

from apps.payments.payments_processor.csv_to_json_processor import csv_to_json
from apps.payments.payments_processor.bank_statements_writer import write_multiple_bank_statements

# Create your views here.
class ManualPolicyPaymentAPIView(generics.CreateAPIView):
    serializer_class = ManualPolicyPaymentSerializer
    permission_classes = [AllowAny]


    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid(raise_exception=True):
            mixin = ManualPaymentProcessingMixin(data=data)
            mixin.run()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class BankStatementPaymentAPIView(generics.CreateAPIView):
    serializer_class = BankStatementPaymentSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            data = request.data
            serializer = self.serializer_class(data=data)
            
            if serializer.is_valid(raise_exception=True):
                statement_file = serializer.validated_data.get("statement_file")
                data = csv_to_json(statement_file)

                statements_data = json.loads(data)

                if len(statements_data) > 10:
                    write_multiple_bank_statements(statements_data)
                else:
                    bank_statement_mixin = BankStatementPaymentProcessMixin(data=statements_data)
                    bank_statement_mixin.run()

                return Response({"msg": "Bank statements uploaded successfully!"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            raise e



class PolicyPremiumViewSet(ModelViewSet):
    queryset = PolicyPremium.objects.all()
    serializer_class = PolicyPremiumSerializer
    permission_classes = [AllowAny]


    def get_queryset(self):
        policy = self.request.query_params.get("policy")

        if policy:
            return self.queryset.filter(policy_id=policy)
        return self.queryset



class BankStatementAPIView(generics.ListAPIView):
    queryset = BankStatement.objects.all()
    serializer_class = BankStatementSerializer

    def get(self, *args, **kwargs):
        policy_number = self.request.query_params.get("policy_number")
        
        statements = BankStatement.objects.all()

        if policy_number:
            statements = BankStatement.objects.filter(policy_number=policy_number)

        serializer = self.serializer_class(instance=statements, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)