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
    create_cycle_status_updates
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

                    PolicyStatusUpdates.objects.create(
                        policy=policy,
                        previous_status="active",
                        next_status="cancelled"
                    )

                    PolicyCancellation.objects.create(**policy_cancellation(policy, reference_reason))
                    cycle = Cycle.objects.filter(membership=membership).first()

                    # Check Cycle status
                    if cycle.status.lower() == "cancelled".lower():
                        create_upload_error_log("Cancel", data, "cancelled_member", "Membership is already cancelled")

                    else:
                        cycle.status = "cancelled"
                        cycle.save()
                        CycleStatusUpdates.objects.create(**create_cycle_status_updates(cycle, "active", "cancelled"))
                        CancellationNotification.objects.create(**cancellation_notification(policy, membership, profile))


            elif action_type.lower() == "Lapsed".lower():
                missed_payment_cycle_types = ["Cancelled", "Lapsed"]
                try:
                    if membership.scheme_group.scheme.is_group_scheme == True:
                        cycle = Cycle.objects.filter(membership=membership).first()

                        if cycle.status.lower() in [x.lower() for x in missed_payment_cycle_types]:
                            create_upload_error_log("Lapsed", data, "lapsed_member", "Membership is already lapsed")

                        else:
                            cycle.status = "lapsed"
                            cycle.save()
                            CycleStatusUpdates.objects.create(**create_cycle_status_updates(cycle, "active", "lapsed"))

                    elif membership.scheme_group.scheme.is_group_scheme == False:
                        cycle = Cycle.objects.filter(membership=membership).first()

                        if cycle.status.lower() in [x.lower() for x in missed_payment_cycle_types]:
                            create_upload_error_log("Lapsed", data, "lapsed_member", "Membership is already lapsed")

                        else:
                            cycle.status = "lapsed"
                            cycle.save()

                            CycleStatusUpdates.objects.create(**create_cycle_status_updates(cycle, "active", "lapsed"))
                        LapseNotification.objects.create(**lapse_notification(membership, profile))
                        
                        policy = membership.scheme_group.policy
                        policy.status = "lapsed"
                        policy.lapse_date = datetime.now().date()
                        policy.save()
                except Exception as e:
                    raise e
        else:
            if data['reference_reason'] == 'Lapsed':
                create_upload_error_log("Lapsed", data, "lapsed_member", "Membership not found!")
            elif data['reference_reason'] == 'Cancel':
                create_upload_error_log("Cancel", data, "cancelled_member", "Membership not found!")

    else:
        if data['reference_reason'] == 'Lapsed':
            create_upload_error_log("Lapsed", data, "lapsed_member", "Profile not found")
        elif data['reference_reason'] == 'Cancel':
            create_upload_error_log("Cancel", data, "cancelled_member", "Profile not found")
