import itertools

from apps.prices.models import MedicalCover, MedicalCoverPricing

INPATIENT_COVER_AMOUNTS = [
    {"cover": 500000, "premium": 500}, 
    {"cover": 1000000, "premium": 1000}, 
    {"cover": 2000000, "premium": 1500}, 
    {"cover": 5000000, "premium": 2000}, 
    {"cover": 1000000, "premium": 2500}
]
OUTPATIENT_COVER_AMOUNTS = [
    {"cover": 0, "premium": 0}, 
    {"cover": 100000, "premium": 100}, 
    {"cover": 150000, "premium": 150}, 
    {"cover": 250000, "premium": 200}
]

medical_cover = MedicalCover.objects.get(name="Senior Citizen Afya")

def create_senior_citizen_cover_pricings():
    combinations = list(itertools.product(INPATIENT_COVER_AMOUNTS, OUTPATIENT_COVER_AMOUNTS))
    pricing_combinations = []
    for combo in combinations:
        inpatient_covers = combo[0]
        outpatient_covers = combo[1]

        pricing_object = {
            "medical_cover": medical_cover,
            "inpatient_cover": inpatient_covers.get("cover"),
            "inpatient_premium": inpatient_covers.get("premium"),
            "outpatient_cover": outpatient_covers.get("cover"),
            "outpatient_premium": outpatient_covers.get("premium") 
        }

        pricing_combinations.append(MedicalCoverPricing(**pricing_object))
    
    MedicalCoverPricing.objects.bulk_create(pricing_combinations)

#create_senior_citizen_cover_pricings()