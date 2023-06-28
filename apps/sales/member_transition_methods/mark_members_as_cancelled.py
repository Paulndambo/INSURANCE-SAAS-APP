from apps.policies.models import (
    Policy,
    PolicyCancellation,
    PolicyStatusUpdates,
    CycleStatusUpdates,
    Cycle,
    CancellationNotification
)
from apps.prices.models import PricingPlan
from apps.sales.share_data_upload_methods.bulk_upload_methods import get_pricing_plan

from apps.users.models import Membership
from apps.sales.share_data_upload_methods.member_transition_methods import (
    cancellation_notification, 
    policy_cancellation,
    create_cycle_status_updates,
    get_membership_profile
)
from apps.sales.share_data_upload_methods.upload_data_error_log import create_upload_error_log


def mark_members_as_cancelled(identification_method: int, identification_number: str, product: int, reference_reason: str, action_type: str):
    data = {
        "identification_number": identification_number,
        "identification_method": identification_method,
        "product": get_pricing_plan(product),
        "reference_reason": reference_reason,
        "action_type": action_type
    }
    profile = get_membership_profile(identification_number)
    if profile:
        pricing_group = PricingPlan.objects.filter(name=get_pricing_plan(product)).first()
        membership = Membership.objects.filter(user=profile.user, scheme_group__pricing_group=pricing_group).first()
        if membership:
            if action_type.lower() == "Cancel".lower():
                if membership.scheme_group.scheme.is_group_scheme == True:
                    cycle = Cycle.objects.filter(membership=membership).first()

                    policy = membership.scheme_group.policy
                
                    if cycle.status.lower() == "cancelled".lower():
                        create_upload_error_log("Cancel", data, "cancelled_member", "Membership is already cancelled")
                        print(f"Cycle: {cycle.id} For Membership: {cycle.membership.id} Is already Cancelled")

                    else:
                        print(f"Cycle: {cycle.id} For Membership: {cycle.membership.id} Is Not Cancelled Yet")
                        cycle.status = "cancelled"
                        cycle.save()
                        CycleStatusUpdates.objects.create(**create_cycle_status_updates(cycle, "active", "cancelled"))
                        CancellationNotification.objects.create(**cancellation_notification(policy, membership, profile, "Group Scheme"))

                else:
                    policy = Policy.objects.filter(id=membership.scheme_group.policy.id).first()
                    if policy:
                        policy.status = "cancelled"
                        policy.save()

                        PolicyStatusUpdates.objects.create(policy=policy, previous_status="active", next_status="cancelled")
                        PolicyCancellation.objects.create(**policy_cancellation(policy, reference_reason))

                    cycle = Cycle.objects.filter(membership=membership).first()
                    if cycle.status.lower() == "cancelled".lower():
                        create_upload_error_log("Cancel", data, "cancelled_member", "Membership is already cancelled")
                        print(f"Cycle: {cycle.id} For Membership: {cycle.membership.id} Is already Cancelled")

                    else:
                        print(f"Cycle: {cycle.id} For Membership: {cycle.membership.id} Is Not Cancelled Yet")
                        cycle.status = "cancelled"
                        cycle.save()
                        CycleStatusUpdates.objects.create(**create_cycle_status_updates(cycle, "active", "cancelled"))
                        CancellationNotification.objects.create(**cancellation_notification(policy, membership, profile, "Retail Scheme"))
        else:
            create_upload_error_log("Cancel", data, "cancelled_member", "Membership not found")
    else:
        create_upload_error_log("Cancel", data, "cancelled_member", "Profile not found")
