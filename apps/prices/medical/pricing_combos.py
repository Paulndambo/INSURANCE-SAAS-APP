import itertools

PH_AGE_GROUPS = [{"ph_age_group": "19-29","premium": 400, "child_premium": 100}, {"ph_age_group":"30-40", "premium": 450, "child_premium": 150}, {"ph_age_group": "41-50", "premium": 500, "child_premium": 200}, {"ph_age_group":"51-65", "premium": 550, "child_premium": 250}]
SPOUSE_AGE_GROUPS = [{"spouse_age_group": "19-29", "premium": 250}, {"spouse_age_goup": "30-40", "premium": 300}, {"spouse_age_group": "41-50", "premium": 350}, {"spouse_age_group": "51-65", "premium": 400}]
INPATIENT_COVER_LEVELS = [500000, 1000000, 3000000, 5000000, 10000000]
OUTPATIENT_COVER_LEVELS = [50000, 60000, 100000, 150000, 200000]

# Generate all possible combinations
combinations = list(itertools.product(PH_AGE_GROUPS, SPOUSE_AGE_GROUPS, INPATIENT_COVER_LEVELS, OUTPATIENT_COVER_LEVELS))

# Print the combinations
pricing_lists = []
for combo in combinations:
    pricing_lists.append(combo)

for x in pricing_lists:
    ph_object = x[0]
    spouse_object = x[1]
    inpatient_cover = x[2]
    outpatient_cover = x[2]

    pricing_object = {
        "ph_age_group": ph_object.get("ph_age_group"),
        "ph_premium": ph_object.get("premium"),
        "child_premium": ph_object.get("child_premium"),
        "spouse_age_group": spouse_object.get("spouse_age_group"),
        "spouse_premium": spouse_object.get("premium"),
        "inpatient_cover": inpatient_cover,
        "outpatient_cover": outpatient_cover
    }
    print(pricing_object)
