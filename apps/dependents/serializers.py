from rest_framework import serializers
from apps.dependents.models import Beneficiary, Dependent


class BeneficiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Beneficiary
        fields = "__all__"


class DependentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dependent
        fields = "__all__"
