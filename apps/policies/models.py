from django.db import models
from apps.core.models import AbstractBaseModel
from apps.users.models import PolicyHolder
from apps.products.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.constants.choice_constants import (
    POLICY_STATUS_CHOICES, 
    POLICY_SUB_STATUS_CHOICES, 
    PAYMENT_PERIOD_CHOICES, 
    CYCLE_STATUS_CHOICES,
    CANCELLATION_ORIGIN
)
from apps.users.utils import is_fake_email


class Policy(AbstractBaseModel):
    insurance_product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    policy_holder = models.ForeignKey(PolicyHolder, null=True, on_delete=models.CASCADE)
    #long_term_price = models.ForeignKey(PolicyPriceEngine, null=True, on_delete=models.CASCADE)
    upgraded_policy = models.OneToOneField('self', blank=True, null=True, on_delete=models.CASCADE)
    policy_number = models.CharField(max_length=255, unique=True)
    policy_name = models.CharField(null=True, max_length=255)
    policy_document = models.FileField(upload_to="policy_documents", null=True)
    welcome_letter = models.FileField(upload_to="policy_welcome_letters", null=True)
    amount = models.FloatField(default=0, validators=[MinValueValidator(limit_value=0), ])
    expiration_date = models.DateField(null=True)
    start_date = models.DateField(null=True)
    activation_date = models.DateField(null=True)
    awaiting_payment_period = models.DateField(null=True)
    payment_due_day = models.IntegerField(default=2, validators=[MinValueValidator(limit_value=0),MaxValueValidator(limit_value=31)])
    payment_frequency = models.CharField(choices=PAYMENT_PERIOD_CHOICES, max_length=255, default='monthly')
    status = models.CharField(choices=POLICY_STATUS_CHOICES, max_length=255, default='created')
    sub_status = models.CharField(choices=POLICY_SUB_STATUS_CHOICES, max_length=32, null=True)
    terms_and_conditions_accepted = models.BooleanField(default=True)
    claim_lodging_awaiting_period = models.IntegerField(default=0)
    lapse_date = models.DateField(null=True)
    change_premium_reason = models.TextField(blank=True, null=True)
    #broker = models.ForeignKey("users.User", null=True, on_delete=models.CASCADE, related_name='broker_policies')
    broker_information = models.JSONField(null=True)
    creator = models.ForeignKey("users.User", null=True, on_delete=models.CASCADE)
    creator_information = models.CharField(null=True, max_length=255)
    damage_reason_expiration = models.DateField(null=True)
    signature = models.FileField(null=True, upload_to="signatures/")
    proxy_purchase = models.BooleanField(default=False)
    terms_and_conditions = models.FileField(upload_to="terms_conditions", null=True) #ForeignKey(InsuranceProductDocument, related_name='policies', null=True, on_delete=models.CASCADE)
    is_group_policy = models.BooleanField(default=False)
    payment_reference = models.CharField(null=True, max_length=100)
    dg_required = models.BooleanField(default=True)
    policy_number_counter = models.IntegerField(default=0)
    config = models.JSONField(default=dict)

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
class Cycle(AbstractBaseModel):
    """
    In all cases Scheme Group has precedence over Membership
    """

    membership = models.ForeignKey("users.Membership", on_delete=models.CASCADE, related_name="cycles", null=True)
    scheme_group = models.ForeignKey("schemes.SchemeGroup", on_delete=models.CASCADE, related_name="cycles", null=True,)
    status = models.CharField(choices=CYCLE_STATUS_CHOICES, max_length=255, default="draft")


#class PolicyStatusUpdates(AbstractBaseModel):
#    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
#    previous_status = models.CharField(max_length=255)
#    next_status = models.CharField(max_length=255)

#    def __str__(self):
#        return self.policy.policy_number

class CycleStatusUpdates(AbstractBaseModel):
    """
    Keep all status updates of Cycle.
    """
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE, related_name="statuses")
    previous_status = models.CharField(max_length=255, choices=CYCLE_STATUS_CHOICES)
    next_status = models.CharField(max_length=255, choices=CYCLE_STATUS_CHOICES)

    def __str__(self):
        return self.next_status


class PolicyCancellation(AbstractBaseModel):
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    status = models.CharField(choices=CANCELLATION_STATUS_CHOICES, max_length=32, default='pending')
    cancellation_origin = models.CharField(choices=CANCELLATION_ORIGIN, max_length=32, default='customer')
    phone_number = models.CharField(max_length=255, null=True)
    bank_account = models.CharField(max_length=255, null=True)
    branch_code = models.CharField(max_length=255, null=True)
    bank = models.CharField(max_length=255, null=True)
    cancel_reason = models.TextField(null=True, blank=True)
    policy_previous_status = models.CharField(max_length=255)
    refund_amount = models.FloatField(default=0)
    payment_reference = models.FileField(upload_to="payment_references/", null=True)

    def __str__(self):
        return 'Cancellation for policy: {0}'.format(self.policy.policy_number)


class RefundRequest(AbstractBaseModel):
    
    STATUS = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    membership = models.ForeignKey("users.Membership", on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS, max_length=32, default='pending')
    phone_number = models.CharField(max_length=255, null=True)
    bank_account = models.CharField(max_length=255, null=True)
    branch_code = models.CharField(max_length=255, null=True)
    bank = models.CharField(max_length=255, null=True)
    refund_amount = models.FloatField(default=0)


    def __str__(self):
        return 'Refund request for member: {0}'.format(self.membership.member_id)


class LapsePendingPolicy(models.Model):
    RETRY_STAUSES = (
        ('error', 'Error'),
        ('failed', 'Failed'),
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('unknown', 'Unknown'),
    )

    policy = models.ForeignKey(Policy, related_name='lapse_details', on_delete=models.CASCADE)
    lapse_date = models.DateField(auto_now=True)
    retry_on_date = models.DateField(null=True)
    retry_status = models.CharField(choices=RETRY_STAUSES, default='unknown', max_length=32)
    lapsed = models.BooleanField(default=False)
    actioned_by = models.ForeignKey("users.User", null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.policy.policy_number


class PolicyDetails(AbstractBaseModel):
    policy = models.OneToOneField(Policy, related_name='policy_details', on_delete=models.CASCADE)
    extra_premium = models.FloatField(default=0)
    funeral_policy_details = models.JSONField(default=dict)
    activation_details = models.JSONField(default=dict)
    cover_level = models.DecimalField(max_digits=10, decimal_places=2, null=True) #ForeignKey(PackageCoverLevel, related_name='policies', on_delete=models.CASCADE, null=True)
    cancellation_date = models.DateField(null=True)

    def __str__(self):
        return self.policy.policy_number


class CancellationNotification(AbstractBaseModel):
    policy = models.ForeignKey(Policy, on_delete=models.SET_NULL, null=True)
    membership = models.ForeignKey("users.Membership", on_delete=models.SET_NULL, null=True)
    email = models.EmailField(null=True)
    mobile_number = models.CharField(max_length=255, null=True)
    notification_send = models.BooleanField(default=False)
    policy_type = models.CharField(max_length=255, null=True)
    product = models.CharField(max_length=255, null=True)
    is_fake_email = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.is_fake_email = is_fake_email(self.email)
        return super().save()


class LapseNotification(AbstractBaseModel):
    membership = models.ForeignKey(
        "users.Membership", on_delete=models.SET_NULL, null=True)
    email = models.EmailField(null=True)
    mobile_number = models.CharField(max_length=255, null=True)
    notification_send = models.BooleanField(default=False)
    policy_type = models.CharField(max_length=255, null=True)
    policy_number = models.CharField(max_length=255, null=True)
    policy_status = models.CharField(max_length=255, null=True)
    product = models.CharField(max_length=255, null=True)
    premium_expected_date = models.DateField(null=True)
    is_fake_email = models.BooleanField(default=False)

    def __str__(self):
        return self.policy_type


class PolicyStatusUpdates(AbstractBaseModel):
    """
    Keep all status updates of policies.
    """

    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    previous_status = models.CharField(max_length=255, choices=POLICY_STATUS_CHOICES)
    next_status = models.CharField(max_length=255, choices=POLICY_STATUS_CHOICES)
