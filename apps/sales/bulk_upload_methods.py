from apps.users.models import Profile
from datetime import datetime


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
        policy_number_prefix = "NTLF_"
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
    return product_id
