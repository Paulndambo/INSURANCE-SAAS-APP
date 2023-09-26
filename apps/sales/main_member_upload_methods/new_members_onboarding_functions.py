from datetime import datetime


def create_policy(pn_data, start_date, sales_agent, premium, cover_amount):
    policy_object = {
        "policy_number": pn_data["policy_number"],
        "amount": premium,
        "cover_amount": cover_amount,
        "start_date": start_date,
        "payment_due_day": 2,
        "payment_frequency": 'monthly',
        "status": 'active',
        "terms_and_conditions_accepted": True,
        "claim_lodging_awaiting_period": 0,
        "proxy_purchase": False,
        "is_group_policy": True,
        "dg_required": False,
        "config": {},
        "policy_number_counter": pn_data["policy_number_counter"],
        "policy_document": '',
        "welcome_letter": '',
        "sold_by": sales_agent
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


def create_retail_scheme_group(scheme, pricing_plan, pricing_plan_name, first_name, last_name):
    scheme_group_object = {
        "scheme_id": scheme.id,
        "name": f"{first_name} {last_name}",
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


def create_policy_holder(user, first_name, last_name, postal_address, phone_number, identification_method, id_number, gender, date_of_birth):
    id_method = identification_method
    policy_holder_object = {
        "user": user,
        "name": f"{first_name} {last_name}",
        "postal_address": postal_address,
        "physical_address": postal_address,
        "phone_number": phone_number,
        "work_phone": phone_number,
        "id_number": id_number,
        "gender": gender,
        "date_of_birth": date_of_birth
    }
    
    return policy_holder_object


def create_profile(user, first_name, last_name, identification_method, id_number, postal_address, phone_number, gender, date_of_birth):
    id_method = identification_method
    profile_object = {
        "user": user,
        "first_name": first_name,
        "last_name": last_name,
        "id_number": id_number,
        "postal_address": postal_address,
        "physical_address": postal_address,
        "phone_number": phone_number,
        "work_phone": phone_number,
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