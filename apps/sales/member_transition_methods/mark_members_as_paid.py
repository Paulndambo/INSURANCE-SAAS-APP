from apps.users.models import User, Membership, Profile
from apps.schemes.models import SchemeGroup, Scheme
from apps.sales.share_data_upload_methods.bulk_upload_methods import get_pricing_plan
from apps.payments.models import PolicyPremium
from apps.policies.models import Cycle, CycleStatusUpdates
from apps.prices.models import PricingPlan
from apps.sales.share_data_upload_methods.upload_data_error_log import create_upload_error_log
from apps.sales.share_data_upload_methods.member_transition_methods import create_cycle_status_updates, get_membership_profile
from apps.sales.share_data_upload_methods.bulk_upload_methods import get_same_date_next_month

def mark_members_as_paid(identification_method: int, identification_number: str, product: int):
    data = {
        "identification_number": identification_number,
        "identification_method": identification_method,
        "product": get_pricing_plan(product)
    }
    try:
        profile = get_membership_profile(identification_number)
        if profile:
            pricing_group = PricingPlan.objects.filter(name=get_pricing_plan(product)).first()
            membership = Membership.objects.filter(user=profile.user, scheme_group__pricing_group=pricing_group).first()
            
            if membership:
                premium = PolicyPremium.objects.filter(membership=membership).order_by("-expected_date").first()
                policy = membership.scheme_group.policy
                next_payment_date = get_same_date_next_month(premium.expected_date)
                balance = abs(-premium.expected_payment)

                print(f"Membership: {membership.id} Found")
                if premium:
                    print(f"Membership ID: {membership.id}, Premium ID: {premium.id}")
                    premium.status = 'paid'
                    premium.balance = 0
                    premium.save()

                    cycle = Cycle.objects.filter(membership=membership).first()

                    if cycle.status in ["awaiting_payment", "created"]:
                        cycle.status = "active"
                        cycle.save()
                        CycleStatusUpdates.objects.create(**create_cycle_status_updates(cycle, cycle.status, "active"))
                        #CycleStatusUpdates.objects.filter(cycle=cycle).order_by("-created").first()
                        #latest_cycle_status_update.next_status = "active"
                        #latest_cycle_status_update.save()

                    elif cycle.status.lower() == "Lapsed".lower():
                        cycle.status = "active"
                        cycle.save()

                        CycleStatusUpdates.objects.create(**create_cycle_status_updates(cycle, "lapsed", "active"))

                        policy = cycle.membership.scheme_group.policy
                        policy.status = "active"
                        policy.save()

                    elif cycle.status.lower() == "Cancelled".lower():
                        cycle.status = "active"
                        cycle.save()

                        CycleStatusUpdates.objects.create(**create_cycle_status_updates(cycle, "cancelled", "active"))

                        policy = cycle.membership.scheme_group.policy
                        policy.status = "active"
                        policy.save()

                new_premium = PolicyPremium.objects.create(
                    membership=membership,
                    policy=policy,
                    status="future",
                    balance=-abs(premium.expected_payment),
                    expected_payment=premium.expected_payment,
                    expected_date=next_payment_date
                )
                print(f"New Premium: {new_premium.id}, Prev. Date: {premium.expected_date}, Date: {new_premium.expected_date}, Bal: {new_premium.balance}, Amount: {new_premium.expected_payment}")
            else:
                print(f"Membership for {identification_number} Not Found!!")
                create_upload_error_log("paid_member", data, "paid_member", "Membership not found!")
        else:
            print(f"Profile for {identification_number} Not Found!!")
            create_upload_error_log("paid_member", data, "paid_member", "Profile not found!")

    except Exception as e:
        raise e
