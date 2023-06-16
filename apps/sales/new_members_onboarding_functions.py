from apps.sales.bulk_upload_methods import get_next_month_first_date
from datetime import datetime

def create_policy(pn_data):
    policy_object = {
        "policy_number": pn_data["policy_number"],
        "amount": 0,
        "start_date": get_next_month_first_date(),
        "payment_due_day": 2,
        "payment_frequency": 'monthly',
        "status": 'active',
        "terms_and_conditions_accepted": True,
        "claim_lodging_awaiting_period": 0,
        # insurance_product_id:1,
        "proxy_purchase": False,
        "is_group_policy": True,
        "dg_required": False,
        "config": {},
        "policy_number_counter": pn_data["policy_number_counter"],
        "policy_document": '',
        "welcome_letter": ''
    }
    return policy_object


def create_scheme_group(scheme, pricing_plan, pricing_plan_name):
    scheme_group_object = {
        "scheme_id": scheme.id,
        "name": pricing_plan_name,
        "payment_method": "off_platform",
        "period_type": "monthly",
        "period_frequency": 1,
        "pricing_group": pricing_plan,
        "cycle_type": "MEMBER_CYCLE",
        "description": pricing_plan_name,
    }
    return scheme_group_object


def create_user(username, email, first_name, last_name):
    user_object = {
        "username": username,
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "password": "temp_password",
        "is_staff": False,
        "is_superuser": False,
        "is_active": True,
        "role": "individual",
    }
    return user_object



def create_policy_holder(individual_user, first_name, last_name, postal_address, phone_number, identification_method, identification_number, gender, date_of_birth):
    if identification_method == 1:
        policy_holder_object = {
            "individual_user": individual_user,
            "name": f"{first_name} {last_name}",
            "address": postal_address,
            "address1": postal_address,
            "phone_number": phone_number,
            "phone": phone_number,
            "phone1": phone_number,
            "id_number": identification_number,
            "gender": gender,
            "date_of_birth": date_of_birth
        }
    else:
        policy_holder_object = {
            "individual_user": individual_user,
            "name": f"{first_name} {last_name}",
            "address": postal_address,
            "address1": postal_address,
            "phone_number": phone_number,
            "phone": phone_number,
            "phone1": phone_number,
            "passport_number": identification_number,
            "gender": gender,
            "date_of_birth": date_of_birth
        }

    return policy_holder_object


def create_profile(user, first_name, last_name, identification_method, identification_number, postal_address, phone_number, gender, date_of_birth):
    if identification_method == 1:
        profile_object = {
            "user": user,
            "first_name": first_name,
            "last_name": last_name,
            "id_number": identification_number,
            "address": postal_address,
            "address1": postal_address,
            "phone": phone_number,
            "phone1": phone_number,
            "gender":gender,
            "date_of_birth": date_of_birth
        }
    else:
        profile_object = {
            "user": user,
            "first_name": first_name,
            "last_name": last_name,
            "passport_number": identification_number,
            "address": postal_address,
            "address1": postal_address,
            "phone": phone_number,
            "phone1": phone_number,
            "gender": gender,
            "date_of_birth": date_of_birth
        }
    
    return profile_object


def create_membership(user, policy, scheme_group):
    membership_object = {
        "user": user,
        "scheme_group": scheme_group,
        "policy": policy,
        "properties": {}
    }
    return membership_object

def create_membership_pemium(policy, total_premium, membership):
    premium_object = {
        "policy": policy,
        "expected_payment": total_premium,
        "balance": -total_premium,
        "membership": membership,
        "expected_date": datetime.now().date(),
        "status": "unpaid",
    }
    return premium_object


def create_payment(policy, membership, total_premium):
    payment_object = {
        "policy": policy,
        "membership": membership,
        "premium": total_premium,
        "payment_due_date": datetime.now().date()
    }
    return payment_object