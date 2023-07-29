from django.db import transaction

# Apps Imports
from apps.schemes.models import Scheme, SchemeGroup
from apps.policies.models import Policy, PolicyDetails, PolicyHolder, Cycle
from apps.users.models import User, Profile, Membership, MembershipConfiguration
from apps.payments.models import PolicyPayment, PolicyPremium
from apps.prices.models import PricingPlan


from apps.sales.share_data_upload_methods.bulk_upload_methods import get_pricing_plan
from apps.sales.main_member_upload_methods.new_members_onboarding_functions import (
    create_policy, create_profile,
    create_policy_holder, create_user, create_membership, 
    create_payment, create_membership_pemium, create_retail_scheme_group
)
from apps.sales.share_data_upload_methods.member_transition_methods import get_membership_profile, get_membership_policy_holder


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
    def __init__(self, data, product):
        self.data = data
        self.product = product

    def run(self):
        self.__upload_telesales_members()

    @transaction.atomic
    def __upload_telesales_members(self):
        members = self.data
        product = self.product

        scheme = Scheme.objects.get(name="Retail Scheme")

        for data in members:
            pricing_plan = PricingPlan.objects.get(name=get_pricing_plan(product))
            pricing_plan_name = get_pricing_plan(product)

            identification_number = data.identification_number
            identification_method = data.identification_method
            date_of_birth = data.date_of_birth
            first_name = data.firstname
            last_name = data.lastname
            postal_address = data.postal_address
            phone_number = data.mobile_number
            product = product
            gender = data.gender
            username = data.username
            email = data.email
            premium_value = data.premium
            cover_level_value = data.cover_level

            scheme_group = SchemeGroup.objects.create(
                **create_retail_scheme_group(
                    scheme, 
                    pricing_plan, 
                    pricing_plan_name, 
                    first_name, 
                    last_name)
                )

            pn_data = scheme.get_policy_number(pricing_plan_name)
            print(f"PN. Data: {pn_data}")

            policy = Policy.objects.create(
                **create_policy(pn_data)
            )

            scheme_group.policy = policy
            scheme_group.save()

            PolicyDetails.objects.create(
                policy=policy
            )

            user = User.objects.filter(email=email).first()
            if not user:
                print("****************Start of Member sales****************")
                user = User.objects.create(**create_user(username, email, first_name, last_name))
                user.set_password("Password")
                user.save()


            profile = Profile.objects.filter(user=user).first()
            if not profile:
                profile = get_membership_profile(identification_number)
                if not profile:
                    profile = Profile.objects.create(
                        **create_profile(
                            user=user, 
                            first_name=first_name, 
                            last_name=last_name, 
                            identification_method=identification_method, 
                            identification_number=identification_number, 
                            postal_address=postal_address, 
                            phone_number=phone_number, 
                            gender=gender, 
                            date_of_birth=date_of_birth
                        )
                    )
                
                    
                policy_holder = get_membership_policy_holder(identification_number)
                if not policy_holder:
                    policy_holder = PolicyHolder.objects.create(
                        **create_policy_holder(
                            user=user, 
                            first_name=first_name, 
                            last_name=last_name, 
                            postal_address=postal_address, 
                            phone_number=phone_number, 
                            identification_method=identification_method, 
                            identification_number=identification_number, 
                            gender=gender, 
                            date_of_birth=date_of_birth
                        )
                    )
                
    
            membership = Membership.objects.create(**create_membership(user, policy, scheme_group))
            print(f"Membership: {membership.id} Created Successfully!!!")

            
            cover_level = 0
            premium = 0
            if premium_value > 0 and cover_level_value > 0:
                cover_level = calculate_telesales_cover_level_by_premium(int(premium_value))
                premium = calculate_telesales_premium_by_cover_level(int(cover_level_value))

            elif premium_value > 0:
                cover_level = calculate_telesales_cover_level_by_premium(int(premium_value))
                premium = calculate_telesales_premium_by_cover_level(int(cover_level))

            elif cover_level_value > 0:
                premium = calculate_telesales_premium_by_cover_level(int(cover_level_value))
                cover_level = calculate_telesales_cover_level_by_premium(int(premium))

            policy_premium = PolicyPremium.objects.create(**create_membership_pemium(policy, premium, membership))
            print(f"Policy Premium: {policy_premium.id} Created Successfully!!!")

            policy_payment = PolicyPayment.objects.create(**create_payment(policy, membership, premium))
            print(f"Policy Payment: {policy_payment.id} Created Successfully!!")

            membership_configuration = MembershipConfiguration.objects.filter(
                membership=membership, beneficiary__isnull=True).first()
            if membership_configuration:
                membership_configuration.cover_level = cover_level
                membership_configuration.save()
            else:
                membership_configuration = MembershipConfiguration.objects.create(
                    membership=membership, cover_level=cover_level, pricing_plan=pricing_plan)
            print(f"Membership Config: {membership_configuration.id} Created Successfully!!")


            cycle = Cycle.objects.filter(membership=membership).first()
            if not cycle:
                cycle = Cycle.objects.create(membership=membership, scheme_group=scheme_group, status="awaiting_payment")
            print(f"Cycle: {cycle.id} Created Successfully!!!")

          
            data.processed = True
            data.save()
            print("****************End of Member sales****************")
