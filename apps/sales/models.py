from django.db import models
from apps.core.models import AbstractBaseModel


# Create your models here.
class TemporaryMemberData(AbstractBaseModel):
    username = models.EmailField(null=True)
    firstname = models.CharField(max_length=255, null=True)
    lastname = models.CharField(max_length=255, null=True)
    email = models.EmailField(null=True)
    identification_method = models.IntegerField(null=True)
    identification_number = models.CharField(max_length=255, null=True)
    mobile_number = models.CharField(max_length=255, null=True)
    landline = models.CharField(max_length=255, null=True)
    physical_address = models.CharField(max_length=500, null=True)
    postal_address = models.CharField(max_length=500, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=255, null=True, blank=True)
    product = models.IntegerField(null=True)
    cover_level = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    premium = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class TemporaryDependentImport(AbstractBaseModel):
    main_member_identification_number = models.CharField(max_length=255)
    #use_type = models.CharField(max_length=255, null=True)
    relationship = models.CharField(max_length=255, null=True)
    relationship_type = models.CharField(max_length=255, null=True)
    cover_level = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    identification_method = models.IntegerField()
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=255, blank=True, null=True)
    product = models.IntegerField()
    processed = models.BooleanField(default=False)

    def __str__(self):
        return self.firstname + self.lastname


class TemporaryPaidMemberData(AbstractBaseModel):
    identification_number = models.CharField(max_length=255)
    identification_method = models.IntegerField()
    product = models.IntegerField()
    processed = models.BooleanField(default=False)

    def __str__(self):
        return self.identification_number


class TemporaryCancelledMemberData(AbstractBaseModel):
    main_member_identification_number = models.CharField(max_length=255)
    identification_number = models.CharField(max_length=255)
    identification_method = models.IntegerField()
    product = models.IntegerField()
    processed = models.BooleanField(default=False)

    def __str__(self):
        return self.identification_number


UPLOAD_TYPES = (
    ("dependents_and_beneficiaries", "Beneficiaries & Dependents"),
    ("new_members", "New Members"),
    ("paid_members", "Paid Members"),
    ("cancelled_members", "Cancelled Members"),
    ("lapsed_members", "Lapsed Members"),
)

ONBOARDING_MODES = (
    ("instant", "Instant"),
    ("background", "Background"),
)


class TemporaryDataHolding(AbstractBaseModel):
    upload_type = models.CharField(max_length=255, choices=UPLOAD_TYPES)
    upload_data = models.JSONField(default=[])
    onboarding_mode = models.CharField(
        max_length=255, choices=ONBOARDING_MODES, default="background"
    )

    def __str__(self):
        return self.upload_type


class MemberUploadOutcome(AbstractBaseModel):
    identification_number = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    product = models.IntegerField()
    reasons = models.JSONField(default=dict)

    def __str__(self):
        return self.identification_number


class PricingPlanSchemeMapping(AbstractBaseModel):
    name = models.CharField(max_length=255)
    scheme_type = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class FailedUploadData(AbstractBaseModel):
    member = models.JSONField(default=dict)
    member_type = models.CharField(max_length=255)
    reason = models.CharField(max_length=255)

    def __str__(self):
        return self.member_type + ' upload failed'
