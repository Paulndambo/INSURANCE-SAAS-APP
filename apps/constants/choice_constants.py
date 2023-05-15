PAYMENT_METHODS = (
    ("cash", "Cash"),
    ("debit_order", "Debit Order"),
    ("stop_order", "Stop Order"),
    ("manual", "Manual"),
    ("off_platform", "Off Platform"),
    ("payu", "Payu"),
    ("paygate", "Pay Gate"),
)


PAYMENT_PERIOD_CHOICES = (
    ("weekly", "Weekly"),
    ("monthly", "Monthly"),
    ("quarterly", "Quarterly"),
    ("biannual", "Biannual"),
    ("yearly", "Yearly"),
    ("single", "Single"),
)

SCHEME_TYPE_CHOICES = (
    ("retail", "Retail"),
    ("group", "Group"),
)


CYCLE_CHOICE_TYPES = (
    ("member", "Member"),
    ("group", "Group"),
)

ROLE_CHOICES = (
    ("None", "Without role"),
    ("admin", "C2S Admin"),
    ("insurer", "Insurer"),
    ("corporate", "Corporate"),
    ("merchant", "Merchant"),
    ("individual", "Individual"),
    ("report_user", "Report User"),
    ("technician_user", "Technician User"),
    ("foh_user", "FOH User"),
    ("customer_support_user", "Customer Support User"),
    ("funeral_validator", "Funeral Validator"),
    ("brokerage_admin", "Brokerage Admin"),
    ("broker", "Broker"),
    ("claim_validator", "Claim Validator"),
    ("retail_agent", "Retail Agent"),
)
SUB_ROLE_CHOICES = (
    ("dynamic_flow", "Dynamic Flow"),
    ("report_user", "Report User"),
    ("customer_support_user", "Customer Support User"),
)


GENDER_CHOICES = (
    ("male", "Male"),
    ("female", "Female"),
)


PAYMENT_STATUS_CHOICES = (
    ("unpaid", "UnPaid"),
    ("paid", "Paid"),
    ("partial", "Partial"),
    ("future", "Future"),
    ("pending", "Pending"),
)

ACCOUNT_TYPES = (
    ("cheque", "Cheque"),
    ("savings", "Savings"),
    ("transmission", "Transmission"),
)

POLICY_STATUS_CHOICES = (
    ("active", "Active"),
    ("lapsed", "Lapsed"),
    ("cancelled", "Cancelled"),
    ("ntu", "NTU"),
    ("created", "Expired"),
    ("awaiting_payment", "Awaiting Payment"),
    ("draft", "Draft"),
    ("incative", "Inactive"),
)
POLICY_SUB_STATUS_CHOICES = (
    ("lapse_pending", "Lapse Pending"),
)

CYCLE_STATUS_CHOICES = (
    ("draft", "Draft"),
    ("created", "Created"),
    ("active", "Active"),
    ("cancelled", "Cancelled"),
    ("lapsed", "Lapsed"),
    ("inactive", "Incative"),
    ("ntu", "Not Taken Up"),
    ("expired", "Expired"),
    ("awaiting_payment", "Awaiting Payment"),
)

POLICY_CANCELLATION_STATUS = (
    ('pending', 'Pending'),
    ('confirmed', 'Confirmed'),
    ('refunded', 'Refunded'),
    ('cancelled', 'Cancelled'),
)
CANCELLATION_ORIGIN = (
    ('customer', 'Customer'),
    ('insurer', 'Insurer'),
)
