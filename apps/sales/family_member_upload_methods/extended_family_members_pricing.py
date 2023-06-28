from datetime import datetime
from apps.constants.pricing_constants import LEGACY_PRICING_PLANS, SYNERGY_PRICING_PLANS, NON_LEGACY_PRICING_PLANS
from apps.prices.models import PricingPlanExtendedPremiumMapping


def calculate_age(date_of_birth):
    date_today = datetime.utcnow().date()
    birthday = date_of_birth

    years = date_today.year - birthday.year - \
        ((date_today.month, date_today.day) < (birthday.month, birthday.day))
    return years


def check_age_range(pricing_mappings, age):
    extended_premium = 0
    for x in pricing_mappings:
        if age >= x.min_age and age <= x.max_age:
            extended_premium = x.extended_premium

    return extended_premium


def calculate_extended_family_pricing(pricing, cover_level, date_of_birth):
    extended_premium = None
    age = calculate_age(date_of_birth)

    if pricing.lower().lower() in [(x).lower() for x in SYNERGY_PRICING_PLANS]:
        pricing_mapping = PricingPlanExtendedPremiumMapping.objects.filter(pricing_plan='Synergy', cover_level=cover_level)
        extended_premium = check_age_range(pricing_mapping, age)

    elif pricing.lower().lower() in [(x).lower() for x in LEGACY_PRICING_PLANS]:
        pricing_mapping = PricingPlanExtendedPremiumMapping.objects.filter(pricing_plan='Legacy', cover_level=cover_level)
        extended_premium = check_age_range(pricing_mapping, age)

    elif pricing.lower() in [(x).lower() for x in NON_LEGACY_PRICING_PLANS]:
        pricing_mapping = PricingPlanExtendedPremiumMapping.objects.filter(pricing_plan='Non-Legacy', cover_level=cover_level)
        extended_premium = check_age_range(pricing_mapping, age)

    return extended_premium
