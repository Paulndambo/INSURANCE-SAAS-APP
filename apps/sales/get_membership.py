from apps.users.models import Profile, Membership, MembershipConfiguration, User
from apps.sales.bulk_upload_methods import get_pricing_plan

def get_membership(identification_number: str, identification_method: int, product: int):
    try:
        profile = None
        if identification_method == 0:
            profile = Profile.objects.get(passport_number=identification_number)
        elif identification_method == 1:
            profile = Profile.objects.get(id_number=identification_number)
        else:
            raise ValueError("The Identification Method You Provided is Not Known!!!!")

        membership = Membership.objects.filter(user=profile.user, scheme_group__name=get_pricing_plan(product)).first()

        return membership
    except Exception as e:
        raise e


def get_membership_configuration(identification_number: str, identification_method: int, product: int):
    try:
        profile = None
        if identification_method == 0:
            profile = Profile.objects.get(passport_number=identification_number)
        elif identification_method == 1:
            profile = Profile.objects.get(id_number=identification_number)
        else:
            raise ValueError("The Identification Method You Provided is Not Known!!!!")

        membership = Membership.objects.filter(user=profile.user, scheme_group__name=get_pricing_plan(product)).first()
        membership_configuration = MembershipConfiguration.objects.filter(membership=membership, beneficiary__isnull=True).first()
        return membership_configuration
    except Exception as e:
        raise e