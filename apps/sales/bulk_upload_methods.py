from apps.users.models import Profile
from datetime import datetime
from apps.prices.models import PricingPlan


def bulk_policy_upload(row):
    data = {
        "username": row[0],
        "firstname": row[1],
        "lastname": row[2],
        "email": row[3],
        "identification_method": row[4],
        "identification_number": row[5],
        "mobile_number": row[6],
        "landline": row[7],
        "date_of_birth": row[8].replace("/", "-"),
        "physical_address": row[9],
        "postal_address": row[10],
        "gender": row[11],
        "product": row[12],
    }
    return data


def get_policy_number_prefix(pricing_plan_id):
    policy_number_prefix = None

    if pricing_plan_id == 0:
        policy_number_prefix = "SYN_"
    elif pricing_plan_id == 1:
        policy_number_prefix = "NW_"
    elif pricing_plan_id == 2:
        policy_number_prefix = "MBD_"
    elif pricing_plan_id == 3:
        policy_number_prefix = "NWL_"
    elif pricing_plan_id == 4:
        policy_number_prefix = "NTL_"
    elif pricing_plan_id == 5:
        policy_number_prefix = "NMBL_"
    elif pricing_plan_id == 6:
        policy_number_prefix = "NMBD_"
    elif pricing_plan_id == 7:
        policy_number_prefix = "NBSL_"
    elif pricing_plan_id == 8:
        policy_number_prefix = "NTF_"
    elif pricing_plan_id == 9:
        policy_number_prefix = "NKL_"
    elif pricing_plan_id == 10:
        policy_number_prefix = "NTLG_"
    elif pricing_plan_id == 11:
        policy_number_prefix = "NWLG_"
    elif pricing_plan_id == 12:
        policy_number_prefix = "NMBLG_"
    elif pricing_plan_id == 13:
        policy_number_prefix = "NBSLG_"
    elif pricing_plan_id == 14:
        policy_number_prefix = "NMBDG_"
    elif pricing_plan_id == 15:
        policy_number_prefix = "NKLG_"
    elif pricing_plan_id == 16:
        policy_number_prefix = "NTCL_"

    return policy_number_prefix


def get_pricing_plan(pricing_plan_id):
    pricing_plan_name = None

    if pricing_plan_id == 0:
        pricing_plan_name = "Synergy"
    elif pricing_plan_id == 1:
        pricing_plan_name = "Nutun Wellness"
    elif pricing_plan_id == 2:
        pricing_plan_name = "MBD Funeral"
    elif pricing_plan_id == 3:
        pricing_plan_name = "Nutun Wellness Legacy"
    elif pricing_plan_id == 4:
        pricing_plan_name = "Nutun Transact Legacy"
    elif pricing_plan_id == 5:
        pricing_plan_name = "Nutun Munnik Basson Da Gama Inc Legacy"
    elif pricing_plan_id == 6:
        pricing_plan_name = "Nutun MBD Legal Collections Legacy"
    elif pricing_plan_id == 7:
        pricing_plan_name = "Nutun Business Services SA Legacy"
    elif pricing_plan_id == 8:
        pricing_plan_name = "Nutun Telesales Funeral"
    elif pricing_plan_id == 9:
        pricing_plan_name = "Nutun Kwande Legacy"
    elif pricing_plan_id == 10:
        pricing_plan_name = "Nutun Transact Group Scheme"
    elif pricing_plan_id == 11:
        pricing_plan_name = "Nutun Wellness Group Scheme"
    elif pricing_plan_id == 12:
        pricing_plan_name = "Nutun Munnik Basson Da Gama Inc Group Scheme"
    elif pricing_plan_id == 13:
        pricing_plan_name = "Nutun Business Services SA Group Scheme"
    elif pricing_plan_id == 14:
        pricing_plan_name = "Nutun MBD Legal Collections Group Scheme"
    elif pricing_plan_id == 15:
        pricing_plan_name = "Nutun Kwande Group Scheme"
    elif pricing_plan_id == 16:
        pricing_plan_name = "Credit Life"

    return pricing_plan_name


def get_premium_amount(pricing_plan):
    premium = None

    if pricing_plan == "Nutun Wellness":
        premium = 12.00
    elif pricing_plan == "MBD Funeral":
        premium = 15.23
    else:
        premium = 40.00

    return premium


def check_if_user_exists(identification_type, identification_number):
    if identification_type == 1:
        profile = Profile.objects.get(id_number=identification_number)
    else:
        profile = Profile.objects.get(passport_number=identification_number)


def get_product_id_from_pricing_plan(pricing_plan: str):
    product_id = ""
    if pricing_plan.lower() == "Synergy".lower():
        product_id = 0
    elif pricing_plan.lower() == "Nutun Wellness Funeral".lower():
        product_id = 1
    elif pricing_plan.lower() == "MBD Funeral".lower():
        product_id = 2
    elif pricing_plan.lower() == "Nutun Wellness Legacy".lower():
        product_id = 3
    elif pricing_plan.lower() == "Nutun Transact Legacy".lower():
        product_id = 4
    elif pricing_plan.lower() == "Nutun Munnik Basson Da Gama Inc Legacy".lower():
        product_id = 5
    elif pricing_plan.lower() == "Nutun MBD Legal Collections Legacy".lower():
        product_id = 6
    elif pricing_plan.lower() == "Nutun Business Services SA Legacy".lower():
        product_id = 7
    elif pricing_plan.lower() == "Nutun Telesales Funeral".lower():
        product_id = 8
    elif pricing_plan.lower() == "Nutun Kwande Legacy".lower():
        product_id = 9
    elif pricing_plan.lower() == "Nutun Transact Group Scheme".lower():
        product_id = 10
    elif pricing_plan.lower() == "Nutun Wellness Group Scheme".lower():
        product_id = 11
    elif pricing_plan.lower() == "Nutun Munnik Basson Da Gama Inc Group Scheme".lower():
        product_id = 12
    elif pricing_plan.lower() == "Nutun Business Services SA Group Scheme".lower():
        product_id = 13
    elif pricing_plan.lower() == "Nutun MBD Legal Collections Group Scheme".lower():
        product_id = 14
    elif pricing_plan.lower() == "Nutun Kwande Group Scheme".lower():
        product_id = 15
    elif pricing_plan.lower() == "Credit Life".lower():
        product_id = 16
    return product_id


def validate_id_number_length(identification_method, identification_number):
    validated_id_number = ""
    identification_number = str(identification_number)
    if int(identification_method) == 1:
        if len(identification_number) == 13:
            validated_id_number = identification_number
        elif len(identification_number) == 12:
            validated_id_number = f"0{identification_number}"
        elif len(identification_number) == 11:
            validated_id_number = f"00{identification_number}"
        elif len(identification_number) == 10:
            validated_id_number = f"000{identification_number}"
        elif len(identification_number) == 9:
            validated_id_number = f"0000{identification_number}"
        elif len(identification_number) == 8:
            validated_id_number = f"00000{identification_number}"

    elif int(identification_method) == 0:
        validated_id_number = identification_number

    return validated_id_number


def validate_phone_number_length(phone_number):
    validated_phone_number = ""

    if phone_number:
        phone_number = str(phone_number)
        if len(phone_number) == 9:
            validated_phone_number = f"0{phone_number}"

        return validated_phone_number
    else:
        return None


def get_pricing_plan_base_cover(pricing_plan_name: str):
    cover_amount = 0
    try:
        pricing_group = PricingPlan.objects.filter(group=pricing_plan_name).first()
        cover_amount = [x for x in pricing_group.matrix.keys()][0]
        return cover_amount
    except Exception as e:
        raise e
    

def get_next_month_first_date():
    today = date.today()
    return today.replace(day=1)
