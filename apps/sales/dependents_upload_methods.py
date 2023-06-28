from apps.users.models import PolicyHolderRelative, MembershipConfiguration
from apps.sales.models import FailedUploadData


from apps.sales.useful_methods import get_policy_scheme_group_and_membership, get_identification_numbers
from apps.sales.date_formatting_methods import date_format_method

import uuid

child_dependent_types = ["Child", "Son", "Daughter"]
spouse_dependent_types = ["Spouse", "Wife", "Husband", "Partner"]


def dependent_object_constructor(data):
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

    data = {
        "main_member_identification_number": main_member_identification_number, 
        "identification_method": identification_method, 
        "identification_number": identification_number, 
        "product": product, 
        "relationship": relationship, 
        "cover_level": cover_level, 
        "first_name": first_name, 
        "last_name": last_name, 
        "date_of_birth": date_of_birth, 
        "gender": gender
    }

    policy_id, scheme_group_id, membership_id = get_policy_scheme_group_and_membership(
        main_member_identification_number=main_member_identification_number,
        identification_method=identification_method,
        product=product
    )

    id_number, passport_number = get_identification_numbers(identification_method, identification_number)
    relative_id = None

    if relationship.lower() in [x.lower() for x in child_dependent_types]:
        relative = PolicyHolderRelative.objects.filter(relative_name__in=["Child", "child"]).first()
        relative_id = relative.id

    elif relationship.lower() in [x.lower() for x in spouse_dependent_types]:
        relative = PolicyHolderRelative.objects.filter(relative_name__in=["Spouse", "spouse"]).first()
        relative_id = relative.id

    elif relationship.lower() == "stillborn":
        relative = PolicyHolderRelative.objects.filter(relative_name__in=["Stillborn", "stillborn"]).first()
        relative_id = relative.id

    if policy_id and scheme_group_id and membership_id:
        membership_config = MembershipConfiguration.objects.filter(membership_id=membership_id, beneficiary__isnull=True).first()

        if membership_config:
            dependent_object = {
                "guid": uuid.uuid4(),
                "membership_configuration_id": membership_config.id,
                "is_additional_family_member": False,
                "dependent_type": relationship.lower(),
                "dependent_type_notes": "",
                "cover_level": cover_level,
                "age_metric": "years",
                "relative_id": relative_id,
                "relative_option": relationship.lower(),
                "first_name": first_name,
                "last_name": last_name,
                "gender": gender.upper(),
                "date_of_birth": date_of_birth,
                "id_number": id_number,
                "passport_number": passport_number,
                "add_on_premium": 0,
                "is_deleted": False
            }
            return dependent_object
            
        else:
            try:
                FailedUploadData.objects.create(
                    member=data,
                    member_type="dependent",
                    reason="Membership Configuration Not Found",
                )
            except Exception as e:
                raise e
    else:
        try:
            FailedUploadData.objects.create(
                member=data,
                member_type="dependent",
                reason="Membership Not Found",
            )
        except Exception as e:
            raise e

        return None
