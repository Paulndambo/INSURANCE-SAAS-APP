from apps.policies.models import (
    PolicyStatusUpdates,
    CycleStatusUpdates,
    Cycle,
    LapseNotification
)
from apps.prices.models import PricingPlan
from apps.sales.bulk_upload_methods import get_pricing_plan
from apps.users.models import Membership
from datetime import datetime
from apps.sales.models import FailedUploadData
from apps.sales.member_transition_methods import (
    lapse_notification,
    create_cycle_status_updates,
    get_membership_profile
)
from apps.sales.upload_data_error_log import create_upload_error_log


def mark_policy_members_as_lapsed(identification_method: int, identification_number: str, product: int, reference_reason: str, action_type: str):
    data = {
        "identification_number": identification_number,
        "identification_method": identification_method,
        "product": get_pricing_plan(product),
        "reference_reason": reference_reason,
        "action_type": action_type
    }
    missed_payment_cycle_types = ["Cancelled", "Lapsed"]
    profile = get_membership_profile(identification_number)
    if profile:
        pricing_group = PricingPlan.objects.filter(name=get_pricing_plan(product)).first()
        membership = Membership.objects.filter(user=profile.user, scheme_group__pricing_group=pricing_group).first()
        if membership:
            policy = membership.scheme_group.policy
            scheme_group = membership.scheme_group
            if scheme_group.scheme.is_group_scheme == True:
                cycle = Cycle.objects.filter(membership=membership).first()
                if cycle.status.lower() in ["lapsed", "cancelled"]:
                    #create_upload_error_log("Lapsed", data, "lapsed_member", "Membership is already lapsed")
                    FailedUploadData.objects.create(
                        member=data,
                        member_type="lapsed_member",
                        reason= "Membership is already lapsed",
                    )
                else:
                    cycle.status = "lapsed"
                    cycle.save()
                    CycleStatusUpdates.objects.create(**create_cycle_status_updates(cycle, "active", "lapsed"))
                    
                    ## Create Lapse Notification Log
            elif scheme_group.scheme.is_group_scheme == False:
                cycle = Cycle.objects.filter(membership=membership).first()

                if cycle.status.lower() == "lapsed":
                    #create_upload_error_log("Lapsed", data, "lapsed_member", "Membership is already lapsed")
                    FailedUploadData.objects.create(
                        member=data,
                        member_type="lapsed_member",
                        reason= "Membership is already lapsed",
                    )
                    print(f"Cycle ID: {cycle.id}, Membership: {cycle.membership.id},  Cycle Status: {cycle.status}, Cycle Should Be Lapsed")
                else:
                    print(f"Cycle ID: {cycle.id}, Membership: {cycle.membership.id}, Cycle Status: {cycle.status}, Cycle Should Not Be Lapsed")
                    
                    cycle.status = "lapsed"
                    cycle.save()
                    CycleStatusUpdates.objects.create(**create_cycle_status_updates(cycle, "active", "lapsed"))
                    LapseNotification.objects.create(**lapse_notification(membership, profile))
                    PolicyStatusUpdates.objects.create(policy=policy, previous_status="active", next_status="lapsed")

                    #policy = membership.scheme_group.policy
                    policy.status = "lapsed"
                    policy.lapse_date = datetime.now().date()
                    policy.save()
                    
        else:
            FailedUploadData.objects.create(
                member=data,
                member_type="lapsed_member",
                reason= "Membership not found",
            )
            #create_upload_error_log("lapsed_member", data, "lapsed_member", "Membership not found!")
    else:
        FailedUploadData.objects.create(
            member=data,
            member_type="lapsed_member",
            reason= "Profile not found",
        )
        #create_upload_error_log("lapsed_member", data, "lapsed_member", "Profile not found!")
