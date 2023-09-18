def get_policy_number_prefix(pricing_group):
    prefix = ''
    if pricing_group.lower() == "Family Bima".lower():
        prefix = "FB_"
    elif pricing_group.lower() == "Elimu Bima".lower():
        prefix = "EB_"
    elif pricing_group.lower() == "Credit Bima".lower():
        prefix = "CLB_"
    elif pricing_group.lower() == "Mtaa Bima".lower():
        prefix = "MTB_"
    elif pricing_group.lower() == "Chama Bima".lower():
        prefix = "CMB_"
    elif pricing_group.lower() == "Medical Bima".lower():
        prefix = "MDB_"
    elif pricing_group.lower() == "Car Bima".lower():
        prefix = "CB_"
    elif pricing_group.lower() == "Pet Bima".lower():
        prefix = "PET_"

    return prefix
