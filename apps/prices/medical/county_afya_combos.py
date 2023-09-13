import itertools

from apps.prices.models import MedicalCover, MedicalCoverPricing

INPATIENT_COVERS = [100000, 250000, 500000, 1000000]
OUTPATIENT_COVERS = [0, 25000, 40000, 50000]
PH_AGE_GROUPS = [{"ph_age_group": "19-29", "ph_premium": 250}, {"ph_age_group":"30-40", "ph_premium": 300}, {"ph_age_group": "41-50", "ph_premium": 350}, {"ph_age_group":"51-65", "ph_premium": 450}]
SPOUSE_AGE_GROUPS = [{"spouse_age_group": "19-29", "spouse_premium": 100}, {"spouse_age_group": "30-40", "spouse_premium": 150}, {"spouse_age_group": "41-50", "spouse_premium": 200}, {"spouse_age_group": "51-65", "spouse_premium": 250}]

def create_medical_cover_pricings():
    combinations = list(itertools.product(PH_AGE_GROUPS, SPOUSE_AGE_GROUPS, INPATIENT_COVERS, OUTPATIENT_COVERS))

    # Print the combinations
    pricing_lists = []
    for combo in combinations:
        pricing_lists.append(combo)

    medical_cover = MedicalCover.objects.get(name="County Afya")

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
   
        pricing_combinations.append(MedicalCoverPricing(**pricing_object))
    

    MedicalCoverPricing.objects.bulk_create(pricing_combinations)
#create_medical_cover_pricings()