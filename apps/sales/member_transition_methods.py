from apps.users.utils import is_fake_email
from apps.users.models import Profile, Membership
from apps.sales.bulk_upload_methods import validate_id_number_length, validate_phone_number_length
from django.db.models import Q


def policy_cancellation(policy, reference_reason):
    return {
        "policy": policy,
        "cancel_reason": reference_reason if reference_reason else None,
        "policy_previous_status": "active",
        "status": "confirmed",
        "cancellation_origin": "insurer"
    }

def lapse_notification(membership, profile):
    return {
        "membership": membership,
        "email": membership.user.email,
        "mobile_number": profile.phone if profile.phone else profile.phone1,
        "notification_send": False,
        "policy_type": "Retail Scheme",
        "policy_number": membership.scheme_group.policy.policy_number,
        "policy_status": membership.scheme_group.policy.status,
        "is_fake_email": is_fake_email(membership.user.email),
        "product": membership.scheme_group.pricing_group,
    }

def cancellation_notification(policy, membership, profile, policy_type):
    return {
        "policy": policy,
        "membership": membership,
        "email": membership.user.email,
        "mobile_number": profile.phone if profile.phone else profile.phone1,
        "notification_send": False,
        "policy_type": policy_type,
        "product": membership.scheme_group.pricing_group
    }

def create_cycle_status_updates(cycle, previous_status, next_status):
    return {
        "cycle": cycle,
        "previous_status": previous_status,
        "next_status": next_status,
    }

def get_membership_profile(identification_number):
    profile = Profile.objects.filter(Q(id_number=identification_number) | Q(passport_number=identification_number)).first()

    if profile:
        return profile
    else:
        return None


