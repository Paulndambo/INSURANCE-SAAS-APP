from django.db import models
from apps.core.models import AbstractBaseModel
from apps.users.models import PolicyHolder

POLICY_STATUS_CHOICES = (
    ("active", "Active"),
    ("lapsed", "Lapsed"),
    ("cancelled", "Cancelled"),
    ("ntu", "NTU"),
    ("awaiting_payment", "Awaiting Payment"),
)

POLICY_SUB_STATUS_CHOICES = (
    ("lapse_pending", "Lapse Pending"),
)

class Policy(AbstractBaseModel):
    policy_number = models.CharField(max_length=255)
    policy_holder = models.ForeignKey(PolicyHolder, on_delete=models.PROTECT)
    status = models.CharField(max_length=255, choices=POLICY_STATUS_CHOICES)
    sub_status = models.CharField(max_length=255, null=True, choices=POLICY_SUB_STATUS_CHOICES)
    activation_date = models.DateField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    lapse_date = models.DateField(null=True, blank=True)
    policy_document = models.FileField(upload_to="policy_documents/", null=True, blank=True)
    policy_wording = models.FileField(upload_to="policy_wordings/", null=True, blank=True)
    welcome_letter = models.FileField(upload_to="welcome_letters/", null=True, blank=True)
    payment_day = models.IntegerField()
    dg_required = models.BooleanField(default=True)

    def __str__(self):
        return self.policy_number


CANCELLATION_STATUS_CHOICES = (
    ("confirmed", "Confirmed"),
    ("pending", "Pending"),
    ("cancelled", "Cancelled"),
)

CANCELLATION_ORIGIN_CHOICES = (
    ("customer", "Customer"),
    ("insurer", "Insurer"),
)


class PolicyCancellation(AbstractBaseModel):
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    policy_previous_status = models.CharField(max_length=255)
    policy_next_status = models.CharField(max_length=255)
    cancellation_status = models.CharField(max_length=255, choices=CANCELLATION_STATUS_CHOICES)
    cancellation_origin = models.CharField(max_length=255, choices=CANCELLATION_ORIGIN_CHOICES)


    def __str__(self):
        return self.policy.policy_number


class PoliyStatusUpdate(AbstractBaseModel):
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    previous_status = models.CharField(max_length=255)
    next_status = models.CharField(max_length=255)

    def __str__(self):
        return self.policy.policy_number


class InsuredItem(AbstractBaseModel):
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    seller = models.CharField(max_length=255)
    brand_name = models.CharField(max_length=255, null=True)
    model = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    price = models.DecimalField( max_digits=10, decimal_places=2)
    cover_amount = models.DecimalField(max_digits=10, decimal_places=2)
    cover_period = models.CharField(max_length=255)

    def __str__(self):
        return self.name
