from rest_framework import serializers
from apps.users.models import (
    Profile,
    Membership,
    MembershipConfiguration,
    User
)
from apps.policies.models import (
    Policy,
    Cycle,
    CycleStatusUpdates
)
from apps.schemes.models import Scheme, SchemeGroup
from apps.dependents.models import Dependent, Beneficiary
from apps.prices.models import PricingPlan

class PolicyHolderReportSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = Membership
        fields = "__all__"

    def get_name(self, obj):
        name = ''
        user = obj.user
        profile = Profile.objects.filter(user=user).first()
        if profile:
            name = f"{profile.first_name} {profile.last_name}"

        return name