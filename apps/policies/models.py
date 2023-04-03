from django.db import models
from apps.core.models import AbstractBaseModel
from apps.users.models import PolicyHolder
from apps.products.models import Product

POLICY_STATUS_CHOICES = (
    ("active", "Active"),
    ("lapsed", "Lapsed"),
    ("cancelled", "Cancelled"),
    ("ntu", "NTU"),
    ("awaiting_payment", "Awaiting Payment"),
)

POLICY_SUB_STATUS_CHOICES = (("lapse_pending", "Lapse Pending"),)


class Policy(AbstractBaseModel):
    policy_number = models.CharField(max_length=255)
    policy_holder = models.ForeignKey(PolicyHolder, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=255, choices=POLICY_STATUS_CHOICES)
    sub_status = models.CharField(max_length=255, null=True, choices=POLICY_SUB_STATUS_CHOICES)
    activation_date = models.DateField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    lapse_date = models.DateField(null=True, blank=True)
    policy_document = models.FileField(upload_to="policy_documents/", null=True, blank=True)
    policy_wording = models.FileField(upload_to="policy_wordings/", null=True, blank=True)
    welcome_letter = models.FileField(upload_to="welcome_letters/", null=True, blank=True)
    payment_day = models.IntegerField(null=True, blank=True)
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


class PolicyStatusUpdate(AbstractBaseModel):
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    previous_status = models.CharField(max_length=255)
    next_status = models.CharField(max_length=255)

    def __str__(self):
        return self.policy.policy_number


class Cycle(AbstractBaseModel):
    """
    In all cases Scheme Group has precedence over Membership
    """

    CREATED_STATUS = "created"
    DRAFT_STATUS = "draft"
    AWAITING_PAYMENT_STATUS = "awaiting_payment"
    ACTIVE_STATUS = "active"
    CANCEL_STATUS = "cancelled"
    EXPIRED_STATUS = "expired"
    LAPSED_STATUS = "lapsed"
    NOT_TAKEN_UP_STATUS = "ntu"
    INACTIVE_STATUS = "inactive"

    PROGRESSABLE_STATUSES = (
        ACTIVE_STATUS,
        AWAITING_PAYMENT_STATUS,
        LAPSED_STATUS,
    )
    STATUS = (
        (DRAFT_STATUS, "Draft"),
        (CREATED_STATUS, "Created"),
        (AWAITING_PAYMENT_STATUS, "Awaiting payment"),
        (ACTIVE_STATUS, "Active"),
        (CANCEL_STATUS, "Cancelled"),
        (EXPIRED_STATUS, "Expired"),
        (LAPSED_STATUS, "Lapsed"),
        (NOT_TAKEN_UP_STATUS, "Not Taken Up"),
        (INACTIVE_STATUS, "Inactive"),
    )
    membership = models.ForeignKey("users.Membership", on_delete=models.CASCADE, related_name="cycles", null=True)
    scheme_group = models.ForeignKey("schemes.SchemeGroup", on_delete=models.CASCADE, related_name="cycles", null=True,)
    status = models.CharField(choices=STATUS, max_length=255, default=DRAFT_STATUS)


class CycleStatusUpdates(AbstractBaseModel):
    """
    Keep all status updates of Cycle.
    """

    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE, related_name="statuses")
    previous_status = models.CharField(max_length=255, choices=Cycle.STATUS)
    next_status = models.CharField(max_length=255, choices=Cycle.STATUS)
