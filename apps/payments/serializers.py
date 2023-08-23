from rest_framework import serializers
from apps.payments.models import PolicyPremium

class PolicyPremiumSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyPremium
        fields = "__all__"