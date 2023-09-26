from rest_framework import serializers

from apps.payments.models import BankStatement, PolicyPayment, PolicyPremium


class PolicyPremiumSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyPremium
        fields = "__all__"


class BankStatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankStatement
        fields = "__all__"


class PolicyPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyPayment
        fields = "__all__"


class ManualPolicyPaymentSerializer(serializers.Serializer):
    policy_number = serializers.CharField(max_length=255)
    id_number = serializers.CharField(max_length=255)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    premium = serializers.IntegerField(required=False)
    payment_date = serializers.DateField(required=False)
    payment_type = serializers.CharField(max_length=255)



class MultipleManualPaymentSerializer(serializers.Serializer):
    payment_type = serializers.CharField(max_length=255)
    payment_data = serializers.FileField()


class BankStatementPaymentSerializer(serializers.Serializer):
    statement_file = serializers.FileField(max_length=None, allow_empty_file=False)


class LipaNaMpesaSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    amount = serializers.IntegerField(default=0)
    

class LipaNaMpesaCallbackSerializer(serializers.Serializer):
    body = serializers.JSONField(required=False)
