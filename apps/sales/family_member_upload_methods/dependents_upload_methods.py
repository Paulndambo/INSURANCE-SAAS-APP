"""Module Imports"""
import uuid


"""Models Imports"""
from apps.users.models import PolicyHolderRelative, MembershipConfiguration
from apps.sales.models import FailedUploadData
from apps.dependents.models import Dependent


"""Custom Methods Imports"""
from apps.sales.share_data_upload_methods.bulk_upload_methods import get_membership, get_identification_numbers
from apps.sales.share_data_upload_methods.date_formatting_methods import date_format_method


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

    membership = get_membership(main_member_identification_number, product)
    scheme_group = membership.scheme_group
    policy = membership.scheme_group.policy
    id_number, passport_number = get_identification_numbers(identification_method, identification_number)

    relative_id = None
    relative = PolicyHolderRelative.objects.filter(relative_name__in=[relationship, relationship.capitalize()]).first()
    relative_id = relative.id

    if policy and scheme_group and membership:
        membership_config = MembershipConfiguration.objects.filter(
            membership_id=membership.id, beneficiary__isnull=True
        ).first()

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
            dependent = Dependent.objects.create(
                **dependent_object
            )
            print(f"Dependent: {dependent.id} Created Successfully!!")
            
        else:
            try:
                FailedUploadData.objects.create(
                    member=member_data,
                    member_type="dependent",
                    reason="Membership Configuration Not Found",
                )
            except Exception as e:
                raise e
    else:
        try:
            FailedUploadData.objects.create(
                member=member_data,
                member_type="dependent",
                reason="Membership Not Found",
            )
        except Exception as e:
            raise e

        return None
