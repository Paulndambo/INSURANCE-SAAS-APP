from rest_framework import serializers

from apps.policies.models import Policy


class SalesAgentPolicySerializer(serializers.ModelSerializer):
    status_updates = serializers.SerializerMethodField()
    premiums = serializers.SerializerMethodField()
    payments = serializers.SerializerMethodField()
    payment_logs = serializers.SerializerMethodField()
    dependents = serializers.SerializerMethodField()
    beneficiaries = serializers.SerializerMethodField()
    extended_dependents = serializers.SerializerMethodField()
    claims = serializers.SerializerMethodField()
    scheme_group_detais = serializers.ReadOnlyField(source="scheme_group")

    class Meta:
        model = Policy
        fields = "__all__"

    def get_status_updates(self, obj):
        return obj.policystatusupdates.values()

    def get_premiums(self, obj):
        return obj.policypremiums.values()

    def get_payments(self, obj):
        return obj.policypayments.values()

    def get_claims(self, obj):
        return obj.policyclaims.values()

    def get_payment_logs(self, obj):
        return obj.policypaymentlogs.values()

    def get_dependents(self, obj):
        return obj.policydependents.filter(dependent_type__in=["Dependent", "dependent"]).values()

    def get_beneficiaries(self, obj):
        return obj.policybeneficiaries.values()

    def get_extended_dependents(self, obj):
        return obj.policydependents.filter(dependent_type__in=["Extended", "extended"]).values()
