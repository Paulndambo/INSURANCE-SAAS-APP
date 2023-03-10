from apps.policies.models import (
    Policy, 
    PolicyCancellation, 
    PolicyStatusUpdate,
    CycleStatusUpdates,
    Cycle
)
from apps.sales.bulk_upload_methods import (
    get_pricing_plan
)

from apps.users.models import User, Profile, Membership

def mark_members_as_cancelled(identification_method: int, id_number: str, product: int, reference_reason: str):

    profile = ''
    if identification_method == 1:
        profile = Profile.objects.filter(id_number=id_number).first()
    else:
        profile = Profile.objects.filter(passport_number=id_number).first()

    membership = Membership.objects.filter(user=profile.user, scheme_group__name=get_pricing_plan(product)).first()

    if membership.scheme_group.scheme__name == 'Group Scheme':
        cycle = Cycle.objects.filter(membership=membership).first()
        cycle.status = "cancelled"
        cycle.save()

        CycleStatusUpdates.objects.create(
            cycle=cycle,
            previous_status="active",
            next_status="cancelled",
        )
    else:
        policy = Policy.objects.get(id=membership.scheme_group.policy.id)
        policy.status="cancelled"
        policy.save()

        PolicyStatusUpdate.objects.create(
            policy=policy, 
            previous_status="active",
            next_status="cancelled"
        )

        PolicyCancellation.objects.create(
            policy=policy,
            policy_next_status="cancelled",
            policy_previous_status="active",
            cancellation_status="confirmed",
            cancellation_origin="insurer"
        )

        cycle = Cycle.objects.filter(membership=membership).first()
        cycle.status = "cancelled"
        cycle.save()

        CycleStatusUpdates.objects.create(
            cycle=cycle,
            previous_status="active",
            next_status="cancelled",
        )
