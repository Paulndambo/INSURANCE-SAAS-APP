from rest_framework import serializers

from apps.policies.models import Policy


class CustomerPolicySerializer(serializers.ModelSerializer):
    status_updates = serializers.SerializerMethodField()
    premiums = serializers.SerializerMethodField()
    payments = serializers.SerializerMethodField()
    payment_logs = serializers.SerializerMethodField()
    dependents = serializers.SerializerMethodField()
    beneficiaries = serializers.SerializerMethodField()
    extended_dependents = serializers.SerializerMethodField()
    claims = serializers.SerializerMethodField()
    scheme_group_detais = serializers.ReadOnlyField(source="scheme_group")
    membership_details = serializers.SerializerMethodField()

    class Meta:
        model = Policy
        fields = "__all__"

    def get_status_updates(self, obj):
        return obj.policystatusupdates.values()

    def get_membership_details(self, obj):
        user = self.context["request"].user
        membership = user.usermembership.filter(policy=obj).values()
        return membership

    def get_premiums(self, obj):
        user = self.context["request"].user
        membership = user.usermembership.filter(policy=obj).first()
        return membership.membershipprems.values()

    def get_payments(self, obj):
        user = self.context["request"].user
        membership = user.usermembership.filter(policy=obj).first()
        return membership.membershippayments.values()

    def get_claims(self, obj):
        user = self.context["request"].user
        membership = user.usermembership.filter(policy=obj).first()
        return membership.membershipclaims.values()

    def get_payment_logs(self, obj):
        user = self.context["request"].user
        membership = user.usermembership.filter(policy=obj).first()
        return membership.paymentlogs.values()

    def get_dependents(self, obj):
        user = self.context["request"].user
        membership = user.usermembership.filter(policy=obj).first()
        return membership.dependents.filter(dependent_type__in=["Dependent", "dependent"]).values()

    def get_beneficiaries(self, obj):
        user = self.context["request"].user
        membership = user.usermembership.filter(policy=obj).first()
        return membership.beneficiaries.values()

    def get_extended_dependents(self, obj):
        user = self.context["request"].user
        membership = user.usermembership.filter(policy=obj).first()
        return membership.dependents.filter(dependent_type__in=["Extended", "extended"]).values()
