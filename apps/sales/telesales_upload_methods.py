from django.db import connection, transaction
from datetime import datetime, date

from apps.sales.bulk_upload_methods import (
    get_policy_number_prefix,
    get_pricing_plan
)
from apps.sales.date_formatting_methods import date_format_method

# Apps Imports
from apps.schemes.models import Scheme, SchemeGroup
from apps.policies.models import (
    Policy,
    PolicyDetails,
    PolicyHolder,
    Cycle,
    CycleStatusUpdates,
)
from apps.users.models import (
    User,
    IndividualUser,
    Profile,
    Membership,
    MembershipConfiguration,
)
from apps.payments.models import PolicyPayment, PolicyPremium
from apps.prices.models import PricingPlan


def calculate_telesales_premium_by_cover_level(cover_level):
    cover_level_premium = 0

    if cover_level == 5000:
        cover_level_premium = 20
    elif cover_level == 10000:
        cover_level_premium = 38
    elif cover_level == 20000:
        cover_level_premium = 74

    return cover_level_premium


def calculate_telesales_cover_level_by_premium(premium):
    cover_level = 0

    if premium == 20:
        cover_level = 5000
    if premium == 38:
        cover_level = 10000
    if premium == 74:
        cover_level = 20000

    return cover_level


class BulkTelesalesUploadMixin(object):
    def __init__(self, data):
        self.data = data

    def run(self):
        self.__upload_telesales_members()

    @transaction.atomic
    def __upload_telesales_members(self):
        members = self.data
        scheme = Scheme.objects.get(name="Retail Scheme")

        for data in members.upload_data:
            pricing_plan = PricingPlan.objects.get(
                name=get_pricing_plan(data["product"]))

            identification_number = data.get("identification number") if data.get(
                "identification number") else data.get("identification_number")
            identification_method = data.get("identification method") if data.get(
                "identification method") else data.get("identification_method")
            date_of_birth = data.get("date of birth") if data.get(
                "date of birth") else data.get("date_of_birth")
            first_name = data.get("firstname") if data.get(
                "firstname") else data.get("first_name")
            last_name = data.get("lastname") if data.get(
                "lastname") else data.get("last_name")
            postal_address = data.get("postal address") if data.get(
                "postal address") else data.get("postal_address")
            phone_number = data.get("mobile number") if data.get(
                "mobile number") else data.get("mobile_number")
            product = data.get("product")
            gender = data.get("gender")
            username = data.get("username")
            email = data.get("email")
            premium_value = data.get("premium")
            cover_level_value = data.get("cover_level") if data.get(
                "cover_level") else data.get("cover level")

            scheme_group = SchemeGroup.objects.create(
                scheme_id=scheme.id,
                name=f"{first_name} {last_name}",
                payment_method="debit_order",
                period_type="monthly",
                period_frequency=1,
                pricing_group=pricing_plan.name,
                cycle_type="member",
                description=get_pricing_plan(product),
            )

            last_policy = Policy.objects.last()

            policy = Policy.objects.create(
                policy_number=f"{get_policy_number_prefix(product)}{last_policy.id+1}",
                amount=0,
                start_date=datetime.now().date(),
                payment_due_day=2,
                payment_frequency='monthly',
                status='active',
                terms_and_conditions_accepted=True,
                claim_lodging_awaiting_period=0,
                insurance_product_id=1,
                proxy_purchase=False,
                is_group_policy=True,
                dg_required=False,
                config={},
                policy_number_counter=1,
                policy_document='',
                welcome_letter=''
            )

            scheme_group.policy = policy
            scheme_group.save()

            PolicyDetails.objects.create(
                policy=policy
            )

            user = User.objects.filter(email=email).first()

            if not user:
                user_obj = {
                    "username": username,
                    "email": email,
                    "first_name": first_name,
                    "last_name": last_name,
                    "password": "temp_password",
                    "is_staff": False,
                    "is_superuser": False,
                    "is_active": True,
                    "role": "individual",
                }
                print("****************Start of Member sales****************")
                user = User.objects.create(**user_obj)
                user.save()

            individual_user = IndividualUser.objects.filter(user=user).first()

            if not individual_user:
                individual_user = IndividualUser.objects.create(user=user)
                individual_user.save()

            profile = Profile.objects.filter(user=user).first()

            if not profile:
                if identification_method == 1:

                    profile = Profile.objects.filter(
                        id_number=identification_number).first()

                    if not profile:
                        profile = Profile.objects.create(
                            user=user,
                            first_name=first_name,
                            last_name=last_name,
                            id_number=identification_number,
                            address=postal_address,
                            address1=postal_address,
                            phone=phone_number,
                            phone1=phone_number,
                            gender=gender,
                            date_of_birth=date_format_method(date_of_birth)
                        )
                        profile.save()
                else:
                    profile = Profile.objects.filter(
                        passport_number=identification_number).first()
                    if not profile:
                        profile = Profile.objects.create(
                            user=user,
                            first_name=first_name,
                            last_name=last_name,
                            passport_number=identification_number,
                            address=postal_address,
                            address1=postal_address,
                            phone=phone_number,
                            phone1=phone_number,
                            gender=gender,
                            date_of_birth=date_format_method(date_of_birth)
                        )
                        profile.save()

            policy_holder = PolicyHolder.objects.filter(
                individual_user=individual_user).first()

            if not policy_holder:
                if identification_method == 1:

                    policy_holder = PolicyHolder.objects.filter(
                        id_number=identification_number).first()

                    if not policy_holder:
                        policy_holder = PolicyHolder.objects.create(
                            individual_user=individual_user,
                            name="{first_name} {last_name}",
                            address=postal_address,
                            address1=postal_address,
                            phone_number=phone_number,
                            phone=phone_number,
                            phone1=phone_number,
                            id_number=identification_number,
                            gender=gender,
                            date_of_birth=date_format_method(date_of_birth)
                        )
                        policy_holder.save()
                else:
                    policy_holder = PolicyHolder.objects.filter(
                        passport_number=identification_number).first()
                    if not policy_holder:
                        policy_holder = PolicyHolder.objects.create(
                            individual_user=individual_user,
                            name=f"{first_name} {last_name}",
                            address=postal_address,
                            address1=postal_address,
                            phone_number=phone_number,
                            phone=phone_number,
                            phone1=phone_number,
                            passport_number=identification_number,
                            gender=gender,
                            date_of_birth=date_format_method(date_of_birth)
                        )
                        policy_holder.save()

            membership = Membership.objects.create(
                user=user,
                scheme_group=scheme_group,
                # policy=policy,
                properties={}
            )
            membership.save()

            print(f"Membership: {membership.id} Created Successfully!!!")

            premium_value = data.get("premium")
            cover_level_value = data.get("cover_level")

            cover_level = 0
            premium = 0

            if premium_value and cover_level_value:
                cover_level = calculate_telesales_cover_level_by_premium(
                    int(premium_value))
                premium = calculate_telesales_premium_by_cover_level(
                    int(cover_level_value))

            elif premium_value:
                cover_level = calculate_telesales_cover_level_by_premium(
                    int(premium_value))
                premium = calculate_telesales_premium_by_cover_level(
                    int(cover_level))

            elif cover_level_value:
                premium = calculate_telesales_premium_by_cover_level(
                    int(cover_level_value))
                cover_level = calculate_telesales_cover_level_by_premium(
                    int(premium))

            policy_premium = PolicyPremium.objects.create(
                policy=policy,
                expected_payment=premium,
                balance=-premium,
                membership=membership,
                expected_date=datetime.now().date(),
                status="unpaid",
            )

            print(
                f"Policy Premium: {policy_premium.id} Created Successfully!!!")

            policy_payment = PolicyPayment.objects.create(
                policy=policy,
                membership=membership,
                premium=premium,
                payment_due_date=datetime.now().date(),
            )

            print(
                f"Policy Payment: {policy_payment.id} Created Successfully!!")

            membership_configuration = MembershipConfiguration.objects.filter(
                membership=membership, beneficiary__isnull=True).first()
            if membership_configuration:
                membership_configuration.cover_level = cover_level
                membership_configuration.save()
            else:
                membership_configuration = MembershipConfiguration.objects.create(
                    membership=membership, cover_level=cover_level, pricing_plan=pricing_plan
                )

            print(
                f"Membership Config: {membership_configuration.id} Created Successfully!!")

            cycle = Cycle.objects.filter(membership=membership).first()

            if not cycle:
                cycle = Cycle.objects.create(
                    membership=membership, scheme_group=scheme_group, status="awaiting_payment"
                )

            print(f"Cycle: {cycle.id} Created Successfully!!!")

            CycleStatusUpdates.objects.create(
                cycle=cycle, previous_status="created", next_status="awaiting_payment"
            )
            print("****************End of Member sales****************")