from apps.policies.models import (
    Policy,
    PolicyCancellation,
    PolicyStatusUpdates,
    CycleStatusUpdates,
    Cycle,
    CancellationNotification,
    LapseNotification
)
from apps.sales.bulk_upload_methods import (
    get_pricing_plan
)
from apps.sales.models import FailedUploadData

from apps.users.models import Profile, Membership
from apps.users.utils import is_fake_email
from datetime import datetime
from apps.sales.member_transition_methods import (
    lapse_notification, 
    cancellation_notification, 
    policy_cancellation,
    create_cycle_status_updates,
    get_membership_profile
)
from apps.sales.upload_data_error_log import create_upload_error_log


def mark_members_as_cancelled(identification_method: int, identification_number: str, product: int, reference_reason: str, action_type: str):
    data = {
        "identification_number": identification_number,
        "identification_method": identification_method,
        "product": get_pricing_plan(product),
        "reference_reason": reference_reason,
        "action_type": action_type
    }
    profile = get_membership_profile(identification_method, identification_number)
    if profile:
        membership = Membership.objects.filter(user=profile.user, scheme_group__pricing_group=get_pricing_plan(product)).first()
        if membership:
            if action_type.lower() == "Cancel".lower():
                if membership.scheme_group.scheme.is_group_scheme == True:
                    cycle = Cycle.objects.filter(membership=membership).first()

                    policy = Policy.objects.get(id=membership.scheme_group.policy.id)
                    policy.status = "cancelled"
                    policy.save()

                    if cycle.status.lower() == "cancelled".lower():
                        create_upload_error_log("Cancel", data, "cancelled_member", "Membership is already cancelled")

                    else:
                        cycle.status = "cancelled"
                        cycle.save()
                        CycleStatusUpdates.objects.create(**create_cycle_status_updates(cycle, "active", "cancelled"))
                    
                        CancellationNotification.objects.create(**cancellation_notification(policy, membership, profile))

                else:
                    policy = Policy.objects.get(id=membership.scheme_group.policy.id)
                    policy.status = "cancelled"
                    policy.save()

                    PolicyStatusUpdates.objects.create(policy=policy, previous_status="active", next_status="cancelled")

                    PolicyCancellation.objects.create(**policy_cancellation(policy, reference_reason))
                    cycle = Cycle.objects.filter(membership=membership).first()
                    if cycle.status.lower() == "cancelled".lower():
                        create_upload_error_log("Cancel", data, "cancelled_member", "Membership is already cancelled")

                    else:
                        cycle.status = "cancelled"
                        cycle.save()
                        CycleStatusUpdates.objects.create(**create_cycle_status_updates(cycle, "active", "cancelled"))
                        CancellationNotification.objects.create(**cancellation_notification(policy, membership, profile))


    else:
        if data['reference_reason'] == 'Lapsed':
            create_upload_error_log("Lapsed", data, "lapsed_member", "Profile not found")
        elif data['reference_reason'] == 'Cancel':
            create_upload_error_log("Cancel", data, "cancelled_member", "Profile not found")
