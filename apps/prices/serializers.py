from rest_framework import serializers
from apps.prices.models import PricingPlan


class PricingPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingPlan
        fields = "__all__"