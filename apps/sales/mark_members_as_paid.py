from apps.users.models import User, Membership, Profile
from apps.schemes.models import SchemeGroup, Scheme
from apps.sales.bulk_upload_methods import get_pricing_plan
from apps.payments.models import PolicyPayment, PolicyPremium
from apps.sales.get_membership import get_membership, get_membership_configuration


def mark_members_as_paid(identification_number: str, identification_method: int, id_number: str, product: int):

    try:
        # profile = ''
        # if identification_method == 1:
        #    profile = Profile.objects.filter(id_number=id_number).first()
        # else:
        #    profile = Profile.objects.filter(passport_number=id_number).first()
        # if profile:
        #    membership = Membership.objects.filter(user=profile.user, scheme_group__name=get_pricing_plan(product)).first()
        #    premium = PolicyPremium.objects.filter(membership=membership).order_by("-expected_date").first()
        membership = get_membership(identification_number, identification_method, product)

        premium = PolicyPremium.objects.filter(membership=membership).order_by("-expected_date").first()
        if premium:
            print(f"Membership ID: {membership.id}, Premium ID: {premium.id}")
            premium.status = 'paid'
            premium.balance = 0
            premium.save()
            print("Premium: ", premium)

        else:
            raise ValueError("The membership does not have a membership premium")

    except Exception as e:
        raise e
