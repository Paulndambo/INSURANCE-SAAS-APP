# Generated by Django 4.1.1 on 2023-06-15 12:51

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("policies", "0001_initial"),
        ("schemes", "0001_initial"),
        ("prices", "0001_initial"),
        ("dependents", "0001_initial"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("token", models.CharField(max_length=255, null=True)),
                ("token_expiration_date", models.DateTimeField(null=True)),
                ("activation_date", models.DateTimeField(null=True)),
                (
                    "email",
                    models.EmailField(
                        error_messages={
                            "unique": "A user with that email already exists."
                        },
                        max_length=254,
                        unique=True,
                    ),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[
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
                        ],
                        default="individual",
                        max_length=32,
                    ),
                ),
                (
                    "sub_role",
                    models.CharField(
                        choices=[
                            ("dynamic_flow", "Dynamic Flow"),
                            ("report_user", "Report User"),
                            ("customer_support_user", "Customer Support User"),
                        ],
                        max_length=32,
                        null=True,
                    ),
                ),
                ("image", models.ImageField(null=True, upload_to="user_images/")),
                ("sent_emails", models.IntegerField(default=0)),
                ("password_expiration_date", models.DateField(null=True)),
                ("reset_password", models.BooleanField(default=False)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="IndividualUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Membership",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("member_id", models.UUIDField(default=uuid.uuid4, unique=True)),
                ("description", models.TextField(null=True)),
                (
                    "membership_status",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("draft", "Draft"),
                            ("created", "Created"),
                            ("active", "Active"),
                            ("cancelled", "Cancelled"),
                        ],
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "membership_certificate",
                    models.FileField(
                        blank=True, null=True, upload_to="membership_certificates"
                    ),
                ),
                (
                    "membership_certificate_generated",
                    models.BooleanField(default=False),
                ),
                (
                    "membership_welcome_letter",
                    models.FileField(
                        blank=True, null=True, upload_to="membership_welcome_letters/"
                    ),
                ),
                ("properties", models.JSONField(default=dict)),
                (
                    "policy",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="policies.policy",
                    ),
                ),
                (
                    "scheme_group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="schemes.schemegroup",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="PolicyHolderRelative",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("relative_name", models.CharField(max_length=255)),
                ("relative_key", models.CharField(max_length=255, unique=True)),
                ("degree_of_separation", models.IntegerField()),
                (
                    "use_type",
                    models.CharField(
                        choices=[
                            ("main_member", "Main Member"),
                            ("dependent", "Dependent"),
                            ("beneficiary", "Beneficiary"),
                            ("parents", "Parents"),
                            ("stillborn", "Stillborn"),
                        ],
                        default="dependent",
                        max_length=128,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("first_name", models.CharField(blank=True, max_length=255)),
                ("last_name", models.CharField(blank=True, max_length=255)),
                ("id_number", models.CharField(max_length=255, null=True, unique=True)),
                (
                    "identification_number",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "registration_number",
                    models.CharField(max_length=255, null=True, unique=True),
                ),
                (
                    "passport_number",
                    models.CharField(max_length=255, null=True, unique=True),
                ),
                ("date_of_birth", models.DateField(null=True)),
                ("occupation", models.TextField(null=True)),
                ("nationality", models.CharField(max_length=120, null=True)),
                (
                    "gender",
                    models.CharField(
                        choices=[("male", "Male"), ("female", "Female")],
                        max_length=60,
                        null=True,
                    ),
                ),
                ("address", models.CharField(blank=True, max_length=255, null=True)),
                ("address1", models.CharField(blank=True, max_length=255, null=True)),
                ("phone", models.CharField(blank=True, max_length=255, null=True)),
                ("phone1", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="PolicyHolder",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "phone_number",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("id_number", models.CharField(max_length=255, null=True, unique=True)),
                (
                    "registration_number",
                    models.CharField(max_length=255, null=True, unique=True),
                ),
                (
                    "passport_number",
                    models.CharField(max_length=255, null=True, unique=True),
                ),
                (
                    "identification_number",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("date_of_birth", models.DateField(null=True)),
                ("occupation", models.TextField(null=True)),
                ("nationality", models.CharField(max_length=120, null=True)),
                (
                    "gender",
                    models.CharField(
                        choices=[("male", "Male"), ("female", "Female")],
                        max_length=60,
                        null=True,
                    ),
                ),
                ("address", models.CharField(blank=True, max_length=255, null=True)),
                ("address1", models.CharField(blank=True, max_length=255, null=True)),
                ("phone", models.CharField(blank=True, max_length=255)),
                ("phone1", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "individual_user",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.individualuser",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="MembershipStatusUpdates",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                ("previous_status", models.CharField(max_length=255)),
                ("next_status", models.CharField(max_length=255)),
                (
                    "membership",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.membership",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="MembershipConfiguration",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                (
                    "cover_level",
                    models.DecimalField(decimal_places=2, max_digits=10, null=True),
                ),
                (
                    "beneficiary",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="dependents.beneficiary",
                    ),
                ),
                (
                    "membership",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.membership",
                    ),
                ),
                (
                    "pricing_plan",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="prices.pricingplan",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
