from apps.users.models import User, Membership, Profile
from apps.schemes.models import SchemeGroup, Scheme
from apps.sales.bulk_upload_methods import get_pricing_plan
from apps.payments.models import PolicyPayment, PolicyPremium
from apps.policies.models import Cycle


def mark_members_as_paid(identification_method: int, identification_number: str, product: int):
    try:
        profile = ''
        if identification_method == 1:
            profile = Profile.objects.filter(
                id_number=identification_number).first()
        else:
            profile = Profile.objects.filter(
                passport_number=identification_number).first()
        if profile:
            membership = Membership.objects.filter(
                user=profile.user, scheme_group__pricing_group=get_pricing_plan(product)).first()
            premium = PolicyPremium.objects.filter(
                membership=membership).order_by("-expected_date").first()

            if premium:
                print(f"Membership ID: {membership.id}, Premium ID: {premium.id}")
                premium.status = 'paid'
                premium.balance = 0
                premium.save()

                cycle = Cycle.objects.filter(membership=membership).first()
                if cycle.status in ["awaiting_payment", "created"]:
                    cycle.status = "active"
                    cycle.save()
            # print("Premium: ", premium)

        else:
            # print(f"ID No: {id_number} has no profile yet")
            pass

    except Exception as e:
        raise e
