from apps.sales.queries import query
from django.db import connection, transaction
from datetime import datetime

from apps.sales.bulk_upload_methods import (
    get_policy_number_prefix,
    get_premium_amount,
    get_pricing_plan,
    get_product_id_from_pricing_plan,
    validate_id_number_length,
    validate_phone_number_length
)


##Apps Imports
from apps.schemes.models import Scheme, SchemeGroup
from apps.policies.models import (
    Policy, PolicyCancellation, PolicyHolder, Cycle, CycleStatusUpdates
)
from apps.users.models import (
    User, IndividualUser, Profile, Membership, MembershipConfiguration
)
from apps.payments.models import PolicyPayment, PolicyPremium
from apps.prices.models import PricingPlan
class BulkMembersOnboardingMixin(object):
    def __init__(self, data):
        self.data = data

    
    def run(self):
        self.__create_scheme_group()

    @transaction.atomic
    def __create_scheme_group(self):
        """
        : Create Scheme Group & Policy
        """
        members = self.data
        first_member = members.upload_data[0]

        pricing_plan = PricingPlan.objects.get(
            name=get_pricing_plan(first_member["product"])
        )

        scheme_group = SchemeGroup.objects.create(
            scheme_id=2,
            name=get_pricing_plan(first_member["product"]),
            payment_method="off_platform",
            period_type="monthly",
            period_frequency=1,
            pricing_group=pricing_plan,
            cycle_type="member",
            description=get_pricing_plan(first_member["product"])
        )

        policy = Policy.objects.create(
            policy_number=f"{get_policy_number_prefix(first_member['product'])}{scheme_group.id}",
            start_date=datetime.now(),
            payment_day=2,
            status='created',
            dg_required=False,

        )

        scheme_group.policy = policy
        scheme_group.save()

        members_data = members.upload_data

        for data in members_data:
            email = data["email"]
            user = User.objects.filter(email=email).first()

            if not user:
                user_obj = {
                    "username": data["username"],
                    "email": data["email"],
                    "first_name": data["firstname"],
                    "last_name": data["lastname"],
                    "password": "temp_password",
                    "is_staff": False,
                    "is_superuser": False,
                    "is_active": True,
                    "role": "individual"
                }
                print("****************Start of Member Onboarding****************")
                user = User.objects.create(**user_obj)
                user.save()

            individual_user = IndividualUser.objects.filter(user=user).first()

            if not individual_user:
                individual_user = IndividualUser.objects.create(user=user)
                individual_user.save()

            profile = Profile.objects.filter(user=user).first()

            if not profile:
                if data["identification_method"] == 1:
                    profile = Profile.objects.create(
                        user=user,
                        first_name=data["firstname"],
                        last_name=data["lastname"],
                        id_number=data["identification_number"],
                        physical_address=data["postal_address"],
                        postal_address=data["postal_address"],
                        phone_number=data["mobile_number"],
                        work_phone_number=data["mobile_number"],
                        home_phone_number=data["landline"],
                        gender=data['gender'],
                        date_of_birth=data['date_of_birth'].replace("/", "-")
                    )
                    profile.save()
                else:
                    profile = Profile.objects.create(
                        user=user,
                        first_name=data["firstname"],
                        last_name=data["lastname"],
                        passport_number=data["identification_number"],
                        physical_address=data["postal_address"],
                        postal_address=data["postal_address"],
                        phone_number=data["mobile_number"],
                        work_phone_number=data["mobile_number"],
                        home_phone_number=data["landline"],
                        gender=data['gender'],
                        date_of_birth=data['date_of_birth'].replace("/", "-")
                    )
                    profile.save()

            policy_holder = PolicyHolder.objects.filter(user=user).first()

            if not policy_holder:
                if data["identification_method"] == 1:
                    policy_holder = PolicyHolder.objects.create(
                        user=user,
                        postal_address=data["postal_address"],
                        phone_number=data["mobile_number"],
                        id_number=data["identification_number"],
                        gender=data['gender'],
                        date_of_birth=data['date_of_birth'].replace("/", "-")
                    )
                    policy_holder.save()
                else:
                    policy_holder = PolicyHolder.objects.create(
                        user=user,
                        postal_address=data["postal_address"],
                        passport_number=data["identification_number"],
                        gender=data['gender'],
                        ddate_of_birth=data['date_of_birth'].replace("/", "-"),
                        phone_number=data["mobile_number"]
                    )
                    policy_holder.save()

                
            #pricing_plan = PricingPlan.objects.get(group=scheme_group.pricing_group)

            membership = Membership.objects.create(
                user=user,
                scheme_group=scheme_group,
                policy=policy,
            )
            membership.save()

            print(f"Membership: {membership.id} Created Successfully!!!")

            # create policy payment
            total_premium = pricing_plan.total_premium

            policy_premium = PolicyPremium.objects.create(
                policy=policy,
                expected_payment=total_premium,
                balance=-total_premium,
                membership=membership,
                expected_date=datetime.now().date(),
                status="unpaid",
            )

            print(f"Policy Premium: {policy_premium.id} Created Successfully!!!")

            policy_payment = PolicyPayment.objects.create(
                policy=policy,
                membership=membership,
                premium=total_premium,
                payment_due_date=datetime.now().date(),
            )

            print(f"Policy Payment: {policy_payment.id} Created Successfully!!")

            membership_configuration = MembershipConfiguration.objects.create(
                membership=membership,
                cover_level=50000,
                pricing_plan=pricing_plan
            )
            membership_configuration.save()

            print(f"Membership Config: {membership_configuration.id} Created Successfully!!")

            cycle = Cycle.objects.filter(membership=membership).first()

            if not cycle:
                cycle = Cycle.objects.create(
                    membership=membership,
                    scheme_group=scheme_group,
                    status='active'
                )

            print(f"Cycle: {cycle.id} Created Successfully!!!")

            CycleStatusUpdates.objects.create(
                cycle=cycle,
                previous_status='awaiting_payment',
                next_status='active'
            )
            print("****************End of Member Onboarding****************")
