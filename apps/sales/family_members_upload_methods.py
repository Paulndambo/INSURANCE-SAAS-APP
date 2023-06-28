from apps.dependents.models import Beneficiary, Dependent
from apps.users.models import MembershipConfiguration, Membership
from apps.sales.useful_methods import get_policy_scheme_group_and_membership
from apps.sales.beneficiaries_upload_methods import beneficiary_object_constructor
from apps.sales.dependents_upload_methods import dependent_object_constructor
from apps.sales.extended_family_members_upload import extended_dependent_object_constructor


def upload_dependents(data):
    try:
        dependent = dependent_object_constructor(data)
        if dependent:
            Dependent.objects.create(**dependent)
        else:
            print("The Membership Does Not Exist!!!")
    except Exception as e:
        raise e


def upload_beneficiaries(data):
    try:
        beneficiary = beneficiary_object_constructor(data)
        if beneficiary:
            Beneficiary.objects.create(**beneficiary)
        else:
            print("The membership for the family member does not exists yet!!!")
    except Exception as e:
        raise e


def upload_extended_family_members(data):
    try:
        extended_dependent = extended_dependent_object_constructor(data)
        if extended_dependent:
            Dependent.objects.create(**extended_dependent)
        else:
            print("The membership for the family member does not exists yet!!!")
    except Exception as e:
        raise e
