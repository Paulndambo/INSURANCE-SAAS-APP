from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from apps.core.models import AbstractBaseModel
from apps.policies.models import Policy
from apps.users.models import MembershipConfiguration, PolicyHolderRelative

DEPENDENT_TYPE = (
    ("dependent", "Dependent"),
    ("extended", "Extended"),
)

AGE_METRIC_CHOICES = (
    ("weeks", "Weeks"),
    ("months", "Months"),
    ("years", "Years"),
)

GENDER_CHOICES = (("female", "Female"), ("male", "Male"))


# Create your models here.
class Beneficiary(AbstractBaseModel):
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, null=True)
    relative = models.ForeignKey(PolicyHolderRelative, on_delete=models.CASCADE, null=True)
    relationship = models.CharField(max_length=255, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255, null=True)
    email = models.EmailField(null=True)
    passport_number = models.CharField(max_length=255, null=True)
    id_number = models.CharField(max_length=255, null=True)
    address = models.TextField(null=True)
    is_deleted = models.BooleanField(default=False)
    date_of_birth = models.DateField(null=True)
    gender=models.CharField(max_length=255, choices=GENDER_CHOICES, null=True)
    membership = models.ForeignKey("users.Membership", on_delete=models.SET_NULL, null=True, blank=True)
    schemegroup = models.ForeignKey("schemes.SchemeGroup", on_delete=models.SET_NULL, null=True, blank=True)
    guardian_or_trustee_first_name = models.CharField(max_length=255, null=True)
    guardian_or_trustee_last_name = models.CharField(max_length=255, null=True)
    guardian_or_trustee_phone_number = models.CharField(max_length=255, null=True)
    guardian_or_trustee_date_of_birth = models.DateField(null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Dependent(AbstractBaseModel):

    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, null=True)
    schemegroup = models.ForeignKey("schemes.SchemeGroup", on_delete=models.SET_NULL, null=True, blank=True)
    membership = models.ForeignKey("users.Membership", null=True, on_delete=models.CASCADE)
    membership_configuration = models.ForeignKey("users.MembershipConfiguration", on_delete=models.CASCADE, null=True)
    is_additional_family_member = models.BooleanField(default=False)
    dependent_type = models.CharField(max_length=200, choices=DEPENDENT_TYPE, null=True)
    dependent_type_notes = models.TextField(null=True, blank=True)
    cover_level = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    age_min = models.PositiveSmallIntegerField(null=True)
    age_max = models.PositiveSmallIntegerField(null=True)
    age_metric = models.CharField(max_length=100, choices=AGE_METRIC_CHOICES)
    relative = models.ForeignKey(PolicyHolderRelative, on_delete=models.CASCADE, null=True)
    relative_option = models.CharField(max_length=200, null=True)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    gender = models.CharField(max_length=200, choices=GENDER_CHOICES, null=True)
    date_of_birth = models.DateField()
    guid = models.CharField(max_length=200, null=True)
    id_number = models.CharField(max_length=255, null=True)
    email = models.EmailField(null=True)
    passport_number = models.CharField(max_length=255, null=True)
    add_on_premium = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, blank=True
    )
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


RELATIVE_TYPE_CHOICES = (
    ("spouse", "Spouse"),
    ("child", "Child"),
    ("extended", "Extended"),
    ("stillborn", "Stillborn")
)

MEMBER_TYPE_CHOICES = (
    ("dependent", "Dependent"),
    ("extended", "Extended")
)

PRICING_GROUP = (
    ("credit", "Credit Life"),
    ("funeral", "Funeral"),
    ("group", "Group"),
    ("retail", "Retail"),
)

class FamilyMemberPricing(AbstractBaseModel):
    pricing_group = models.CharField(max_length=255, choices=PRICING_GROUP)
    member_type = models.CharField(max_length=255, choices=MEMBER_TYPE_CHOICES)
    relative_type = models.CharField(max_length=255, choices=RELATIVE_TYPE_CHOICES)
    min_age = models.IntegerField(default=0)
    max_age = models.IntegerField(default=0)
    cover_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    premium = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.relative_type
    

"""
@receiver(post_save, sender=Beneficiary)
def create_membership_configuration(sender, instance, created, **kwargs):
    if created:
        MembershipConfiguration.objects.create(
            beneficiary=instance,
            membership=instance.membership,
            cover_level=0,
            pricing_plan=instance.schemegroup.pricing_plan
        )
"""