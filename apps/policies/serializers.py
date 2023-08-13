from rest_framework import serializers
from apps.policies.models import Policy, PolicyCancellation, Cycle, CycleStatusUpdates


class PolicySerializer(serializers.ModelSerializer):
    scheme_group_detais = serializers.ReadOnlyField(source="scheme_group")
    class Meta:
        model = Policy
        fields = "__all__"

    

class PolicyCancellationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyCancellation
        fields = "__all__"


# class PolicyStatusUpdatesSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = PolicyStatusUpdates
#        fields = "__all__"


class CycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cycle
        fields = "__all__"



class CycleStatusUpdatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CycleStatusUpdates
        fields = "__all__"