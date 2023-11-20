from rest_framework import serializers

from apps.dependents.models import Beneficiary, Dependent
from apps.policies.models import Cycle, CycleStatusUpdates, Policy
from apps.prices.models import PricingPlan
from apps.schemes.models import Scheme, SchemeGroup
from apps.users.models import (Membership, MembershipConfiguration, Profile,
                               User)


class PolicyHolderReportSerializer(serializers.ModelSerializer):
    created = serializers.SerializerMethodField()
    modified = serializers.SerializerMethodField()
    policy_number = serializers.SerializerMethodField()
    scheme_group = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    membership_premium = serializers.SerializerMethodField()
    balance = serializers.SerializerMethodField()
    premium_due_date = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()
    id_number = serializers.SerializerMethodField()
    passport_number = serializers.SerializerMethodField()
    policyholder_email = serializers.SerializerMethodField()
    lapse_date = serializers.SerializerMethodField()
    payment_frequency = serializers.SerializerMethodField()
    awaiting_payment_period = serializers.SerializerMethodField()
    activation_date = serializers.SerializerMethodField()
    policy_status = serializers.SerializerMethodField()
    insurance_product = serializers.SerializerMethodField()
    
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
    
    def get_created(self, obj):
        return obj.created.date()
    
    def get_modified(self, obj):
        return obj.modified.date()
    
    def get_policy_status(self, obj):
        return obj.policy.status if obj.policy else ''
    
    def get_insurance_product(self, obj):
        return 'Pavi Wellness Funeral'
    

    def get_lapse_date(self, obj):
        return obj.policy.lapse_date if obj.policy else ''
    

    def get_activation_date(self, obj):
        return obj.policy.activation_date if obj.policy else ''
    

    def get_payment_frequency(self, obj):
        return obj.policy.payment_frequency if obj.policy else ''
    

    def get_awaiting_payment_period(self, obj):
        return obj.policy.awaiting_payment_period if obj.policy else ''
    

    def get_policyholder_email(self, obj):
        return obj.user.email


    def get_phone_number(self, obj):
        profile = Profile.objects.filter(user=obj.user).first()
        return profile.phone if profile.phone else profile.phone1
    

    def get_id_number(self, obj):
        profile = Profile.objects.filter(user=obj.user).first()
        return profile.id_number if profile.id_number else ''
    
    
    def get_passport_number(self, obj):
        profile = Profile.objects.filter(user=obj.user).first()
        return profile.passport_number if profile.passport_number else ''


    def get_policy_number(self, obj):
        return obj.policy.policy_number if obj.policy else ''
    
    
    def get_scheme_group(self, obj):
        return obj.scheme_group.description if obj.scheme_group.description else ''
    

    def get_membership_premium(self, obj):
        premium = obj.membershipprems.order_by("-created").first()
        return premium.expected_payment if premium and premium.expected_payment else 0
    
    def get_balance(self, obj):
        premium = obj.membershipprems.order_by("-created").first()
        return premium.balance if premium and premium.balance else 0
    
    def get_premium_due_date(self, obj):
        premium = obj.membershipprems.order_by("-created").first()
        return premium.expected_date if premium and premium.expected_date else ''