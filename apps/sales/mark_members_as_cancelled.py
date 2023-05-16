from apps.policies.models import (
    Policy,
    PolicyCancellation,
    PolicyStatusUpdates,
    CycleStatusUpdates,
    Cycle,
    CancellationNotification,
    LapseNotification
)
from apps.onboarding.bulk_upload_methods import (
    get_pricing_plan
)
from apps.onboarding.models import FailedUploadData

from apps.users.models import Profile, Membership
from apps.users.utils import is_fake_email
from datetime import datetime


def mark_members_as_cancelled(identification_method: int, identification_number: str, product: int, reference_reason: str, action_type: str):

    profile = ''
    if identification_method == 1:
        profile = Profile.objects.filter(id_number=identification_number).first()
    else:
        profile = Profile.objects.filter(passport_number=identification_number).first()

    if profile:
        membership = Membership.objects.filter(user=profile.user, scheme_group__pricing_group=get_pricing_plan(product)).first()
        if membership:
            if action_type.lower() == "Cancel".lower():
                if membership.scheme_group.scheme.is_group_scheme == True:
                    cycle = Cycle.objects.filter(membership=membership).first()
                    cycle.status = "cancelled"
                    cycle.save()

                    CycleStatusUpdates.objects.create(
                        cycle=cycle,
                        previous_status="active",
                        next_status="cancelled",
                    )

                    CancellationNotification.objects.create(
                        policy=policy,
                        membership=membership,
                        email=membership.user.email,
                        mobile_number=profile.phone if profile.phone else profile.phone1,
                        notification_send=False,
                        policy_type="Group Scheme",
                        product=membership.scheme_group.pricing_group    
                    )

                else:
                    policy = Policy.objects.get(id=membership.scheme_group.policy.id)
                    policy.status = "cancelled"
                    policy.save()

                    PolicyStatusUpdates.objects.create(
                        policy=policy,
                        previous_status="active",
                        next_status="cancelled"
                    )

                    PolicyCancellation.objects.create(
                        policy=policy,
                        cancel_reason=reference_reason if reference_reason else None,
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
                    CancellationNotification.objects.create(
                        policy=policy,
                        membership=membership,
                        email=membership.user.email,
                        mobile_number=profile.phone if profile.phone else profile.phone1,
                        notification_send=False,
                        policy_type="Retail Scheme",
                        product=membership.scheme_group.pricing_group        
                    )
            elif action_type.lower() == "Lapsed".lower():
                try:
                    if membership.scheme_group.scheme.is_group_scheme == False:
                        lapse_notif = LapseNotification(
                            membership=membership, 
                            email=membership.user.email,
                            mobile_number=profile.phone if profile.phone else profile.phone1,
                            notification_send=False,
                            policy_type="Retail Scheme",
                            policy_number=membership.scheme_group.policy.policy_number,
                            policy_status=membership.scheme_group.policy.status,
                            is_fake_email=is_fake_email(membership.user.email),
                            product=membership.scheme_group.pricing_group,

                        )
                        lapse_notif.save()

                        policy = membership.scheme_group.policy
                        policy.status = "lapsed"
                        policy.lapse_date = datetime.now().date()
                        policy.save()
                except Exception as e:
                    raise e
        else:
            data = {
                "identification_number": identification_number,
                "product": product,
                "reference_reason": reference_reason
            }
            try:
                FailedUploadData.objects.create(
                    member=data,
                    member_type="cancellation data",
                    reason="membership not found"
                )
            except Exception as e:
                raise e
    else:
        data = {
                "identification_number": identification_number,
                "product": product,
                "reference_reason": reference_reason
        }
        try:
            FailedUploadData.objects.create(
                member=data,
                member_type="cancellation data",
                reason="profile not found"
            )
        except Exception as e:
            raise e
