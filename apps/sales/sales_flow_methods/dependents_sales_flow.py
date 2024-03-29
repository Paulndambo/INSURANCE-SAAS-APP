from apps.users.models import PolicyHolderRelative, MembershipConfiguration
from apps.sales.models import FailedUploadData


from apps.sales.share_data_upload_methods.bulk_upload_methods import get_membership
from apps.sales.share_data_upload_methods.date_formatting_methods import date_format_method
import uuid

child_dependent_types = ["Child", "Son", "Daughter"]
spouse_dependent_types = ["Spouse", "Wife", "Husband", "Partner"]


def dependent_object_constructor(data):
    main_member_identification_number = data.get("main_member_identification_number") if data.get("main_member_identification_number") else data.get("main member identification number")
    identification_method = data.get("identification method") if data.get("identification method") else data.get("identification_method")
    product = data.get("product")
    identification_number = data.get("identification_number") if data.get("identification_number") else data.get("identification number")
    relationship = data.get("relationship")
    cover_level = data.get("cover_level") if data.get("cover_level") else data.get("cover level")
    first_name = data.get("firstname") if data.get("firstname") else data.get("first_name")
    last_name = data.get("lastname") if data.get("lastname") else data.get("last_name")
    date_of_birth = data.get("date of birth") if data.get("date of birth") else data.get("date_of_birth")
    gender = data.get("gender")

    policy_id, scheme_group_id, membership_id = get_membership(
        main_member_identification_number=main_member_identification_number,
        identification_method=identification_method,
        product=product
    )

    relative_id = None

    if relationship.lower() in [x.lower() for x in child_dependent_types]:
        relative = PolicyHolderRelative.objects.filter(
            relative_name__in=["Child", "child"]).first()
        relative_id = relative.id

    elif relationship.lower() in [x.lower() for x in spouse_dependent_types]:
        relative = PolicyHolderRelative.objects.filter(
            relative_name__in=["Spouse", "spouse"]).first()
        relative_id = relative.id

    if policy_id and scheme_group_id and membership_id:
        membership_config = MembershipConfiguration.objects.filter(
            membership_id=membership_id, beneficiary__isnull=True).first()

        if membership_config:

            if identification_method == 0:
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
                    "date_of_birth": date_format_method(date_of_birth),
                    "passport_number": identification_number,
                    "add_on_premium": 0,
                    "is_deleted": False
                }
                return dependent_object

            elif identification_method == 1:
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
                    "date_of_birth": date_format_method(date_of_birth),
                    "id_number": identification_number,
                    "identification_number": identification_number,
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
