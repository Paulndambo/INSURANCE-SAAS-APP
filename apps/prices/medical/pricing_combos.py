import itertools

from apps.prices.models import MedicalCover, MedicalCoverPricing

PH_AGE_GROUPS = [{"ph_age_group": "19-29","ph_premium": 400}, {"ph_age_group":"30-40", "ph_premium": 450}, {"ph_age_group": "41-50", "ph_premium": 500}, {"ph_age_group":"51-65", "ph_premium": 550}]
SPOUSE_AGE_GROUPS = [{"spouse_age_group": "19-29", "spouse_premium": 250}, {"spouse_age_group": "30-40", "spouse_premium": 300}, {"spouse_age_group": "41-50", "spouse_premium": 350}, {"spouse_age_group": "51-65", "spouse_premium": 400}]
INPATIENT_COVER_LEVELS = [500000, 1000000, 3000000, 5000000, 10000000]
OUTPATIENT_COVER_LEVELS = [50000, 60000, 100000, 150000, 200000]

# Generate all possible combinations
def create_medical_cover_pricings():
    combinations = list(itertools.product(PH_AGE_GROUPS, SPOUSE_AGE_GROUPS, INPATIENT_COVER_LEVELS, OUTPATIENT_COVER_LEVELS))

    # Print the combinations
    pricing_lists = []
    for combo in combinations:
        pricing_lists.append(combo)

    medical_cover = MedicalCover.objects.first()

    pricing_combinations = []

    for x in pricing_lists:
        ph_object = x[0]
        spouse_object = x[1]
        inpatient_cover = x[2]
        outpatient_cover = x[3]

        pricing_object = {
            "medical_cover": medical_cover,
            "ph_age_group": ph_object.get("ph_age_group"),
            "ph_premium": ph_object.get("ph_premium"),
            "child_premium": 100,
            "spouse_age_group": spouse_object.get("spouse_age_group"),
            "spouse_premium": spouse_object.get("spouse_premium"),
            "inpatient_cover": inpatient_cover,
            "outpatient_cover": outpatient_cover
        }
        #pricing_combinations.append(MedicalCoverPricing(**pricing_object))
    

    #MedicalCoverPricing.objects.bulk_create(pricing_combinations)

