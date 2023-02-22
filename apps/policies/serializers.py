from rest_framework import serializers
from apps.policies.models import Policy, PolicyCancellation, PolicyStatusUpdates


class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = "__all__"


class PolicyCancellationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyCancellation
        fields = "__all__"


class PolicyStatusUpdatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyStatusUpdates
        fields = "__all__"
