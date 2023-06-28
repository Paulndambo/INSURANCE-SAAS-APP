from apps.users.models import PolicyHolderRelative
from apps.sales.models import FailedUploadData


from apps.sales.useful_methods import get_policy_scheme_group_and_membership, get_identification_numbers
from apps.sales.date_formatting_methods import date_format_method




def beneficiary_object_constructor(
    main_member_identification_number: str, identification_method: int, identification_number: str, product: int, relationship: str, 
    first_name: str, last_name: str, phone_number: str, date_of_birth):
    
    
    policy_id, scheme_group_id, membership_id = get_policy_scheme_group_and_membership(
        main_member_identification_number=main_member_identification_number,
        product=product
    )

    id_number, passport_number = get_identification_numbers(identification_method, identification_number)

   
    relative_id = None
    rel_relative = PolicyHolderRelative.objects.filter(relative_name__in=[relationship, relationship.capitalize()]).first()

    if rel_relative:
        relative_id = rel_relative.id
    else:
        ben_relative = PolicyHolderRelative.objects.filter(relative_name__in=["beneficiary", "beneficiary".capitalize()]).first()
        relative_id = ben_relative.id

    if policy_id and scheme_group_id and membership_id:
        beneficiary = {
            "policy_id": policy_id,
            "schemegroup_id": scheme_group_id,
            "membership_id": membership_id,
            "first_name": first_name,
            "last_name": last_name,
            "email": data.get("email"),
            "passport_number": passport_number,
            "id_number": id_number,
            "phone_number": phone_number,
            "date_of_birth": date_format_method(date_of_birth),
            "relative_id": relative_id,
            "address": data.get("address"),
        }

        return beneficiary
    else:
        # TODO write the family member to a list of not uploaded family members
        # not_uploaded_family_members.append(data)
        try:
            FailedUploadData.objects.create(
                member=data,
                member_type="beneficiary",
                reason="membership not found"
            )
        except Exception as e:
            raise e
        return None  # not_uploaded_family_members
