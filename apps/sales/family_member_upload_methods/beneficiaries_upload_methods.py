"""Models Imports"""
from apps.users.models import PolicyHolderRelative
from apps.sales.models import FailedUploadData
from apps.dependents.models import Beneficiary


"""Custom Methods Imports"""
from apps.sales.share_data_upload_methods.bulk_upload_methods import get_membership, get_identification_numbers


def beneficiary_object_constructor(data):
    main_member_identification_number = data.main_member_identification_number
    identification_method = data.identification_method
    identification_number = data.identification_number
    product = data.product
    relationship = data.relationship
    cover_level = data.cover_level
    first_name = data.firstname
    last_name = data.lastname
    date_of_birth = data.date_of_birth
    gender = data.gender

    member_data = {
        "main_member_identification_number": main_member_identification_number, 
        "identification_method": identification_method, 
        "identification_number": identification_number, 
        "product": product, 
        "relationship": relationship, 
        "cover_level": int(cover_level), 
        "first_name": first_name, 
        "last_name": last_name, 
        "gender": gender
    }

    if not identification_number or not first_name or not last_name:
        FailedUploadData.objects.create(
            member=member_data,
            member_type="beneficiary",
            reason="Missing data, the data provided is incomplete!"
        )
    else:    
        membership = get_membership(main_member_identification_number, product)
        if membership:
            scheme_group = membership.scheme_group
            policy = membership.scheme_group.policy
            id_number, passport_number = get_identification_numbers(identification_method, identification_number)

            relative_id = None
            relative = PolicyHolderRelative.objects.filter(relative_name__in=[relationship, relationship.capitalize()]).first()
            if relative:
                relative_id = relative.id

            if policy and scheme_group and membership:
                beneficiary_object = {
                    "policy_id": policy.id,
                    "schemegroup_id": scheme_group.id,
                    "membership_id": membership.id,
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": "",
                    "cover_level": cover_level,
                    "passport_number": passport_number,
                    "id_number": id_number,
                    "phone_number": "",
                    "date_of_birth": date_of_birth,
                    "relative_id": relative_id,
                    "address": "",
                }

                beneficiary = Beneficiary.objects.create(
                    **beneficiary_object
                )
                print(f"Beneficiary: {beneficiary.id} Created Successfully!!")
        else:
            try:
                FailedUploadData.objects.create(
                    member=member_data,
                    member_type="beneficiary",
                    reason="Membership not found"
                )
            except Exception as e:
                raise e
        
