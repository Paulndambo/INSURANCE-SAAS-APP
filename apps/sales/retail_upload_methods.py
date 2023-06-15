from django.db import connection, transaction
from datetime import datetime, date

from apps.sales.bulk_upload_methods import (
    get_policy_number_prefix,
    get_pricing_plan,
    get_pricing_plan_base_cover,
    get_next_month_first_date

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


class BulkRetailMemberOnboardingMixin(object):
    def __init__(self, data):
        self.data = data

    def run(self):
        self.__onboard_retail_members()

    @transaction.atomic
    def __onboard_retail_members(self):

        data = self.data
        scheme = Scheme.objects.get(name="Retail Scheme")
        for member in data:
            identification_number = member.identification_number
            identification_method = member.identification_method
            date_of_birth = member.date_of_birth
            first_name = member.firstname
            last_name = member.lastname
            postal_address = member.postal_address
            phone_number = member.mobile_number
            product = member.product
            gender = member.gender
            email = member.email
            username = member.username

            pricing_plan = PricingPlan.objects.get(name=get_pricing_plan(product))
            pricing_plan_name = get_pricing_plan(product)

            scheme_group = SchemeGroup.objects.create(
                scheme_id=scheme.id,
                name=f"{first_name} {last_name}",
                payment_method="debit_order",
                period_type="monthly",
                period_frequency=1,
                pricing_group=pricing_plan.name,
                cycle_type="member".upper(),
                description=get_pricing_plan(product),
            )

            pn_data = scheme.get_policy_number(pricing_plan_name)
            print(f"PN. Data: {pn_data}")
        
            policy = Policy.objects.create(
                policy_number=pn_data["policy_number"],
                amount=0,
                start_date=get_next_month_first_date(),
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
                policy_number_counter=pn_data["policy_number_counter"],
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
                            date_of_birth=date_of_birth
                        )
                        profile.save()
                else:
                    profile = Profile.objects.filter(passport_number=identification_number).first()
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
                            date_of_birth=date_of_birth
                        )
                        profile.save()

            policy_holder = PolicyHolder.objects.filter(individual_user=individual_user).first()
            # policy_holder_by_identification_number = PolicyHolder.objects.filter(id_number=data["identification number"]).first()

            if not policy_holder:
                if identification_method == 1:

                    policy_holder = PolicyHolder.objects.filter(
                        id_number=identification_number).first()

                    if not policy_holder:
                        policy_holder = PolicyHolder.objects.create(
                            individual_user=individual_user,
                            name=f"{first_name} {last_name}",
                            address=postal_address,
                            address1=postal_address,
                            phone_number=phone_number,
                            phone=phone_number,
                            phone1=phone_number,
                            id_number=identification_number,
                            gender=gender,
                            date_of_birth=date_of_birth
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
                            date_of_birth=date_of_birth
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

            total_premium = pricing_plan.total_premium

            policy_premium = PolicyPremium.objects.create(
                policy=policy,
                expected_payment=total_premium,
                balance=-total_premium,
                membership=membership,
                expected_date=datetime.now().date(),
                status="unpaid",
            )

            print(
                f"Policy Premium: {policy_premium.id} Created Successfully!!!")

            policy_payment = PolicyPayment.objects.create(
                policy=policy,
                membership=membership,
                premium=total_premium,
                payment_due_date=datetime.now().date(),
            )

            print(f"Policy Payment: {policy_payment.id} Created Successfully!!")

            membership_configuration = MembershipConfiguration.objects.filter(
                membership=membership, beneficiary__isnull=True).first()
            if membership_configuration:
                membership_configuration.cover_level = get_pricing_plan_base_cover(
                    pricing_plan.name)
                membership_configuration.save()
            else:
                membership_configuration = MembershipConfiguration.objects.create(
                    membership=membership, cover_level=get_pricing_plan_base_cover(pricing_plan.name), pricing_plan=pricing_plan
                )

            print(
                f"Membership Config: {membership_configuration.id} Created Successfully!!")

            cycle = Cycle.objects.filter(membership=membership).first()

            if not cycle:
                cycle = Cycle.objects.create(
                    membership=membership, scheme_group=scheme_group, status="awaiting_payment"
                )

            print(f"Cycle: {cycle.id} Created Successfully!!!")

            # CycleStatusUpdates.objects.create(
            #    cycle=cycle, previous_status="created", next_status="awaiting_payment"
            # )
            print("****************End of Member sales****************")
