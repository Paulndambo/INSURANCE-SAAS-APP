from django.db import transaction

from apps.prices.models import PricingPlan, PricingPlanSchemeMapping
from apps.sales.family_member_upload_methods.beneficiaries_upload_methods import \
    beneficiary_object_constructor
from apps.sales.family_member_upload_methods.dependents_upload_methods import \
    dependent_object_constructor
from apps.sales.family_member_upload_methods.extended_family_members_upload import \
    extended_dependent_object_constructor
from apps.sales.main_member_upload_methods.group_upload_methods import \
    BulkGroupMembersOnboardingMixin
from apps.sales.main_member_upload_methods.retail_upload_methods import \
    BulkRetailMemberOnboardingMixin
from apps.sales.main_member_upload_methods.telesales_upload_methods import \
    BulkTelesalesUploadMixin
from apps.sales.member_transition_methods.mark_members_as_cancelled import \
    mark_members_as_cancelled
from apps.sales.member_transition_methods.mark_members_as_lapsed import \
    mark_policy_members_as_lapsed
from apps.sales.member_transition_methods.mark_members_as_paid import \
    mark_members_as_paid
from apps.sales.share_data_upload_methods.bulk_upload_methods import \
    get_pricing_plan
from apps.schemes.models import Scheme


class BulkMembersOnboardingMixin(object):
    def __init__(self, data):
        self.data = data

    def run(self):
        self.__onboard_members()

    @transaction.atomic
    def __onboard_members(self):
        group_plans = list(PricingPlanSchemeMapping.objects.filter(scheme_type="group").values_list("name", flat=True))
        retail_plans = list(PricingPlanSchemeMapping.objects.filter(scheme_type="retail").values_list("name", flat=True))
        telesales_plans = list(PricingPlanSchemeMapping.objects.filter(scheme_type="telesales").values_list("name", flat=True))

        first_member = self.data.upload_data[0]
        pricing_plan = PricingPlan.objects.get(name=get_pricing_plan(first_member["product"]))
        pricing_plan_name = pricing_plan.name


        if pricing_plan_name in telesales_plans:
            telesales_mixin = BulkTelesalesUploadMixin(self.data)
            telesales_mixin.run()

        elif pricing_plan_name in retail_plans:
            bulk_retail_mixin = BulkRetailMemberOnboardingMixin(self.data)
            bulk_retail_mixin.run()

        elif pricing_plan_name in group_plans:
            bulk_group_mixin = BulkGroupMembersOnboardingMixin(self.data)
            bulk_group_mixin.run()



class DependentOnboardingMixin(object):
    def __init__(self, data):
        self.data = data

    def run(self):
        self.__onboard_dependent_family_members()


    def __onboard_dependent_family_members(self):
        dependents = self.data

        try:
            for dependent in dependents:
                dependent_object_constructor(dependent)
                dependent.processed = True 
                dependent.save()
        except Exception as e:
            raise e
        

class ExtendedDependentOnboardingMixin(object):
    def __init__(self, data):
        self.data = data  

    def run(self):
        self.__onboard_extended_family_members()


    def __onboard_extended_family_members(self):
        extendent_dependents = self.data 
        try:
            for extendent_dependent in extendent_dependents:
                extended_dependent_object_constructor(extendent_dependent)
                extendent_dependent.processed = True
                extendent_dependent.save()
        except Exception as e:
            raise e
        

class BeneficiaryOnboardingMixin(object):
    def __init__(self, data):
        self.data = data 

    def run(self):
        self.__onboard_member_beneficiaries()


    def __onboard_member_beneficiaries(self):
        beneficiaries = self.data
        try:
            for beneficiary in beneficiaries:
                beneficiary_object_constructor(beneficiary)
                beneficiary.processed = True
                beneficiary.save()
        except Exception as e:
            raise e


class BulkPaidMembersMixin(object):
    def __init__(self, data):
        self.data = data

    def run(self):
        self.__mark_members_as_paid()

    @transaction.atomic
    def __mark_members_as_paid(self):
        try:
            data = self.data
            for member in data:
                mark_members_as_paid(
                    identification_method=member.identification_method,
                    identification_number=member.identification_number,
                    product=member.product
                )
                member.processed = True 
                member.save()
        except Exception as e:
            raise e


class MembersCancellationMixin(object):
    def __init__(self, data):
        self.data = data

    def run(self):
        self.__cancel_membership()

    @transaction.atomic
    def __cancel_membership(self):
        try:
            data = self.data
            for member in data:
                mark_members_as_cancelled(
                    identification_method=member.identification_method,
                    identification_number=member.identification_number,
                    product=member.product,
                    action_type=member.action_type,
                    reference_reason=member.reference_reason
                )
                member.processed = True
                member.save()
        except Exception as e:
            raise e


class BulkLapsedMembersMixin(object):
    def __init__(self, data):
        self.data = data

    def run(self, *args, **kwargs):
        self.__lapse_members()

    @transaction.atomic
    def __lapse_members(self):
        try:
            data = self.data
            for member in data:
                mark_policy_members_as_lapsed(
                    identification_method=member.identification_method,
                    identification_number=member.identification_number,
                    product=member.product,
                    action_type=member.action_type,
                    reference_reason=member.reference_reason
                )
                member.processed = True
                member.save()
        except Exception as e:
            raise e

