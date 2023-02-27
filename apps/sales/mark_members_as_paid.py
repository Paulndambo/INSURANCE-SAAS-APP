from apps.users.models import User, Membership, Profile
from apps.schemes.models import SchemeGroup, Scheme
from apps.sales.bulk_upload_methods import get_pricing_plan
from apps.payments.models import PolicyPayment, PolicyPremium

def mark_members_as_paid(identification_method: int, id_number: str, product: int):

    try:
        profile = ''
        if identification_method == 1:
            profile = Profile.objects.filter(id_number=id_number).first()
        else:
            profile = Profile.objects.filter(passport_number=id_number).first()
        if profile:
            membership = Membership.objects.filter(user=profile.user, scheme_group__name=get_pricing_plan(product)).first()
            premium = PolicyPremium.objects.filter(membership=membership).latest("expected_date")
            print(f"Membership ID: {membership.id}, Premium ID: {premium.id}")
            premium.status='paid'
            premium.save()
            print(f"ID No: {id_number} Profile Found!!")
            
        else:
            print(f"ID No: {id_number} has no profile yet")
            

    except Exception as e:
        raise e
