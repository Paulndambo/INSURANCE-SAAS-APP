from django.db import connection, transaction
from datetime import datetime, date

from apps.sales.bulk_upload_methods import (
    get_pricing_plan
)

from apps.sales.family_members_upload_methods import upload_beneficiaries, upload_dependents, upload_extended_family_members

from apps.sales.mark_members_as_paid import mark_members_as_paid
from apps.sales.mark_members_as_cancelled import mark_members_as_cancelled

from apps.prices.models import PricingPlan, PricingPlanSchemeMapping
from apps.sales.retail_upload_methods import BulkRetailMemberOnboardingMixin
from apps.sales.group_upload_methods import BulkGroupMembersOnboardingMixin
from apps.sales.telesales_upload_methods import BulkTelesalesUploadMixin


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

        #print(pricing_plan_name)
        # print(group_plans)
        if pricing_plan_name in telesales_plans:
            telesales_mixin = BulkTelesalesUploadMixin(self.data)
            telesales_mixin.run()

        elif pricing_plan_name in retail_plans:
            bulk_retail_mixin = BulkRetailMemberOnboardingMixin(self.data)
            bulk_retail_mixin.run()

        elif pricing_plan_name in group_plans:
            bulk_group_mixin = BulkGroupMembersOnboardingMixin(self.data)
            bulk_group_mixin.run()


class FamilyMemberOnboardingMixin(object):
    def __init__(self, data):
        self.data = data

    def run(self):
        self.__onboard_family_members()

    @transaction.atomic
    def __onboard_family_members(self):
        data = self.data.upload_data

        dependent_types = ["Dependent", "Dependant"]

        for x in data:
            if x["relationship_type"].lower() in [x.lower() for x in dependent_types]:
                try:
                    upload_dependents(x)
                except Exception as e:
                    raise e
            elif x["relationship_type"].lower() == "extended":
                try:
                    upload_extended_family_members(x)
                except Exception as e:
                    raise e
            elif x["relationship_type"].lower() == "beneficiary":
                try:
                    upload_beneficiaries(x)
                except Exception as e:
                    raise e


class BulkPaidMembersMixin(object):
    def __init__(self, data):
        self.data = data

    def run(self):
        self.__mark_members_as_paid()

    @transaction.atomic
    def __mark_members_as_paid(self):
        data = self.data
        for member in data:
            identification_method = member.identification_method
            identification_number = member.identification_number
            product = member.product
            try:
                mark_members_as_paid(
                    identification_method=identification_method,
                    identification_number=identification_number,
                    product=product,
                )
            except Exception as e:
                raise e


class MembersCancellationMixin(object):
    def __init__(self, data):
        self.data = data

    def run(self):
        self.__cancel_membership()

    @transaction.atomic
    def __cancel_membership(self):
        data = self.data

        for member in data:
            identification_method = member.identification_method
            identification_number = member.identification_number
            product = member.product
            action_type = member.action_type
            reference_reason = member.reference_reason
            try:
                mark_members_as_cancelled(
                    identification_method=identification_method,
                    identification_number=identification_number,
                    product=product,
                    reference_reason=reference_reason,
                    action_type=action_type
                )
            except Exception as e:
                raise e


class BulkLapsedMembersMixin(object):
    def __init__(self, data):
        data = self.data

    def run(self, *args, **kwargs):
        self.__lapse_members()

    @transaction.atomic
    def __lapse_members(self):
        data = self.data