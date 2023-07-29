"""Model Signals"""
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from apps.users.models import Membership, MembershipConfiguration, User
from apps.policies.models import Cycle, CycleStatusUpdates
from apps.dependents.models import Beneficiary

from rest_framework.authtoken.models import Token

"""
@receiver(post_save, sender=Beneficiary)
def create_membership_configuration(sender, instance, created, **kwargs):
    if created:
        pricing_plan_name = instance.schemegroup.pricing_group.name
        cover_level = 5000 if pricing_plan_name in ["MBD Funeral", "Nutun Wellness", "Nutun Wellness Funeral"] else 50000
        MembershipConfiguration.objects.create(
            beneficiary=instance,
            membership=instance.membership,
            cover_level=cover_level,
            pricing_plan=instance.schemegroup.pricing_group
        )


@receiver(post_save, sender=Membership)
def create_membership_config(sender, instance, created, **kwargs):
    if created:
        pricing_plan_name = instance.scheme_group.pricing_group.name
        cover_level = 5000 if pricing_plan_name in ["MBD Funeral", "Nutun Wellness", "Nutun Wellness Funeral"] else 50000
        MembershipConfiguration.objects.create(
            membership=instance,
            pricing_plan=instance.scheme_group.pricing_group,
            cover_level=cover_level
        )
"""

@receiver(post_save, sender=Membership)
def create_membership_cycle(sender, instance, created, **kwargs):
    if created:
        cycle = Cycle.objects.create(
            membership=instance,
            scheme_group=instance.scheme_group,
            status="awaiting_payment"
        )
        CycleStatusUpdates.objects.create(
            cycle=cycle,
            previous_status="draft",
            next_status="created"
        )
        CycleStatusUpdates.objects.create(
            cycle=cycle,
            previous_status="created",
            next_status="awaiting_payment"
        )


@receiver(post_save, sender=User)
def create_user_token(sender, instance, created, **kwargs):
    if created:
        token = Token.objects.create(user=instance)