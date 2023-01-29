from django.db import models
from apps.core.models import AbstractBaseModel
from apps.users.models import PolicyHolderRelative
from apps.policies.models import Policy

# Create your models here.


class Beneficiary(AbstractBaseModel):
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, null=True)
    relative = models.ForeignKey(PolicyHolderRelative, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255, null=True)
    email = models.EmailField(null=True)
    passport_number = models.CharField(max_length=255, null=True)
    id_number = models.CharField(max_length=255, null=True)
    address = models.TextField(null=True)
    is_deleted = models.BooleanField(default=False)
    date_of_birth = models.DateField(null=True)
    membership = models.ForeignKey('users.Membership', on_delete=models.SET_NULL, null=True, blank=True)
    schemegroup = models.ForeignKey('schemes.SchemeGroup', on_delete=models.SET_NULL, null=True, blank=True)
    # Required for minor beneficiaries
    guardian_or_trustee_first_name = models.CharField(max_length=255, null=True)
    guardian_or_trustee_last_name = models.CharField(max_length=255, null=True)
    guardian_or_trustee_phone_number = models.CharField(max_length=255, null=True)
    guardian_or_trustee_date_of_birth = models.DateField(null=True)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Dependent(AbstractBaseModel):
    DEPENDENT_TYPE = (
        ("main_member", "Main Member"),
        ('spouse', 'Spouse'),
        ('child', 'Child'),
        ('parent', 'Parent'),
        ('extended', 'Additional/Extended Family Member'),
        ('stillborn', 'Stillborn'),
    )

    AGE_METRIC_CHOICES = (
        ('weeks', 'Weeks'),
        ('months', 'Months'),
        ('years', 'Years'),
    )

    GENDER_CHOICES = (
        ("female", "Female"),
        ("male", "Male")
    )

    membership = models.ForeignKey('users.Membership', null=True, on_delete=models.CASCADE)
    is_additional_family_member = models.BooleanField(default=False)
    dependent_type = models.CharField(max_length=200, choices=DEPENDENT_TYPE)
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
    passport_number = models.CharField(max_length=255, null=True)
    add_on_premium = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"
