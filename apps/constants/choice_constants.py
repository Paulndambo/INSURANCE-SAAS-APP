PAYMENT_METHODS = (
    ("cash", "Cash"),
    ("debit_order", "Debit Order"),
    ("stop_order", "Stop Order"),
    ("off_platform", "Off Platform"),
    ("mpesa", "Mpesa"),
    ("manual", "Manual"),
)


PAYMENT_PERIOD_CHOICES = (
    ("weekly", "Weekly"),
    ("monthly", "Monthly"),
    ("quarterly", "Quarterly"),
    ("biannual", "Biannual"),
    ("yearly", "Yearly"),
    ("single", "Single"),
)

PRICING_PLAN_KINDS = (
    ("short_term", "Short Term"),
    ("long_term", "Long Term"),
)

SCHEME_TYPE_CHOICES = (
    ("retail", "Retail"),
    ("group", "Group"),
    ("credit", "Credit"),
    ("pet", "Pet"),
    ("funeral", "funeral"),
)

OBLIGATION_TYPES = (
    ("obligation", "Obligation"),
    ("3rd Party Insurance", "3rd Party Insurance")
)


CYCLE_CHOICE_TYPES = (
    ("member", "Member"),
    ("group", "Group"),
)

ROLE_CHOICES = (
    ("None", "Without role"),
    ("admin", "Admin"),
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
    ("sales_agent", "Sales Agent"),
    ("claim_validator", "Claim Validator"),
    ("retail_agent", "Retail Agent"),
)
SUB_ROLE_CHOICES = (
    ("dynamic_flow", "Dynamic Flow"),
    ("report_user", "Report User"),
    ("customer_support_user", "Customer Support User"),
)


GENDER_CHOICES = (
    ("Male", "Male"),
    ("Female", "Female"),
)


PAYMENT_STATUS_CHOICES = (
    ("unpaid", "UnPaid"),
    ("paid", "Paid"),
    ("partial", "Partial"),
    ("future", "Future"),
    ("pending", "Pending"),
    ("overpayment", "Over Payment"),
)

PAYMENT_TYPE_CHOICES = (
    ("bank", "Bank"),
    ("card", "Card"),
    ("mpesa", "Mpesa"),
    ("manual", "Manual"),
    ("bank_statement", "Bank Statement"),
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
