from rest_framework import serializers
from apps.entities.models import Brokerage, SalesAgent


class BrokerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brokerage
        fields = "__all__"


class SalesAgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesAgent
        fields = "__all__"