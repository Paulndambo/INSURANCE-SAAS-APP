from apps.users.models import Profile, Membership
from apps.sales.bulk_upload_methods import get_pricing_plan
from apps.prices.models import PricingPlanSchemeMapping
from datetime import datetime
from dateutil.relativedelta import relativedelta
from apps.sales.member_transition_methods import get_membership_profile
from apps.prices.models import PricingPlan


def get_same_date_next_month(expected_date):
    next_month = expected_date + relativedelta(months=1)
    day = expected_date.day

    if next_month.day < day:
        next_month = next_month.replace(day=next_month.day - 1)

    return next_month


def get_policy_scheme_group_and_membership(main_member_identification_number: str, product: int):

    membership_id = None
    scheme_group_id = None
    policy_id = None

    profile = get_membership_profile(main_member_identification_number)
    pricing_group = PricingPlan.objects.get(name=get_pricing_plan(product))
    if profile:
        membership = Membership.objects.filter(user=profile.user, scheme_group__pricing_group=pricing_group).first()
        if membership:
            policy_id = membership.scheme_group.policy_id
            scheme_group_id = membership.scheme_group_id
            membership_id = membership.id


    return policy_id, scheme_group_id, membership_id


def get_dependent_cover_level(dependent_type, pricing_plan, dependent_age):
    dependent_cover_level = 0
    retail_plans = list(PricingPlanSchemeMapping.objects.filter(
        scheme_type__in=['retail', 'telesales']).values_list('name', flat=True))
    group_plans = list(PricingPlanSchemeMapping.objects.filter(
        scheme_type__in=['group']).values_list('name', flat=True))

    legacy_plans = [x for x in group_plans if x != "Synergy"]

    child_dependent_types = ["Child", "Son", "Daughter"]
    spouse_dependent_types = ["Spouse", "Wife", "Husband", "Partner"]

    if pricing_plan.lower() in [x.lower() for x in retail_plans]:
        dependent_cover_level = dependent_cover_level

    elif pricing_plan.lower() in [x.lower() for x in group_plans]:
        if pricing_plan.lower() == "Synergy".lower():
            if dependent_type.lower() in [x.lower() for x in spouse_dependent_types]:
                if dependent_age >= 18 and dependent_age <= 65:
                    dependent_cover_level = 35000
                else:
                    dependent_cover_level = 0

            elif dependent_type.lower() in [x.lower() for x in child_dependent_types]:
                if dependent_age >= 14 and dependent_age <= 21:
                    dependent_cover_level = 27000
                elif dependent_age >= 6 and dependent_age <= 13:
                    dependent_cover_level = 18000
                elif dependent_age >= 0 and dependent_age <= 5:
                    dependent_cover_level = 12500

            elif dependent_type.lower() == "Stillborn".lower() and dependent_age < 1:
                dependent_cover_level = 12500

        elif pricing_plan.lower() in [x.lower() for x in legacy_plans]:
            if dependent_type.lower() in [x.lower() for x in spouse_dependent_types]:
                if dependent_age >= 18 and dependent_age <= 65:
                    dependent_cover_level = 50000
                else:
                    dependent_cover_level = 0

            elif dependent_type.lower() in [x.lower() for x in child_dependent_types]:
                if dependent_age >= 14 and dependent_age <= 21:
                    dependent_cover_level = 50000
                elif dependent_age >= 6 and dependent_age <= 13:
                    dependent_cover_level = 25000
                elif dependent_age >= 0 and dependent_age <= 5:
                    dependent_cover_level = 12500

            elif dependent_type.lower() == "Stillborn" and dependent_age < 1:
                dependent_cover_level = 12500

    return dependent_cover_level


def get_extended_family_member_premium(cover_level: int, pricing_plan: str):
    pass



def get_identification_numbers(identification_method: int, identification_number: str):
    id_number = ''
    passport_number = ''
    if identification_method == 0:
        passport_number = identification_number 
    elif identification_method == 1:
        id_number = identification_number
    
    return id_number, passport_number