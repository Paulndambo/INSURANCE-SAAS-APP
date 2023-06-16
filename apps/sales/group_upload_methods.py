from django.db import connection, transaction
from datetime import datetime, date

from apps.sales.bulk_upload_methods import (
    get_policy_number_prefix,
    get_pricing_plan,
    get_pricing_plan_base_cover,
    get_next_month_first_date

)
from apps.sales.date_formatting_methods import date_format_method
from apps.sales.new_members_onboarding_functions import (
    create_policy, create_scheme_group, create_profile, 
    create_policy_holder, create_user, create_membership, create_payment, create_membership_pemium
)


# Apps Imports
from apps.schemes.models import Scheme, SchemeGroup
from apps.policies.models import (
    Policy,
    PolicyDetails,
    PolicyHolder,
    Cycle
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


class BulkGroupMembersOnboardingMixin(object):
    def __init__(self, data, product):
        self.data = data
        self.product = product

    def run(self):
        self.__onboard_group_scheme_members()

    @transaction.atomic
    def __onboard_group_scheme_members(self):
        product = self.product
        data = self.data
        pricing_plan_name = get_pricing_plan(product)

        pricing_plan = PricingPlan.objects.get(name=get_pricing_plan(product))
        scheme = Scheme.objects.get(name="Group Scheme")

        scheme_group = SchemeGroup.objects.create(
            **create_scheme_group(scheme, pricing_plan, pricing_plan_name)
        )

        pn_data = scheme.get_policy_number(pricing_plan_name)
        print(f"PN. Data: {pn_data}")

        policy = Policy.objects.create(**create_policy(pn_data))

        scheme_group.policy = policy
        scheme_group.save()

        PolicyDetails.objects.create(policy=policy)

        for member in data:
            email = member.email
            phone_number = member.mobile_number
            username = member.username
            first_name = member.firstname
            last_name = member.lastname
            identification_method = member.identification_method
            identification_number = member.identification_number
            postal_address = member.postal_address
            physical_address = member.physical_address
            date_of_birth = member.date_of_birth
            gender = member.gender

            user = User.objects.filter(email=email).first()

            if not user:
                user = User.objects.create(**create_user(username, email, first_name, last_name))
                
            individual_user = IndividualUser.objects.filter(user=user).first()

            if not individual_user:
                individual_user = IndividualUser.objects.create(user=user)
                individual_user.save()


            profile = Profile.objects.filter(user=user).first()
            if not profile:
                if identification_method == 1:
                    profile = Profile.objects.filter(id_number=identification_number).first()
                    if not profile:
                        profile = Profile.objects.create(
                            **create_profile(user, first_name, last_name, identification_method, 
                                identification_number, postal_address, phone_number, gender, date_of_birth)) 
                else:
                    profile = Profile.objects.filter(passport_number=identification_number).first()
                    if not profile:
                        profile = Profile.objects.create(
                            **create_profile(user, first_name, last_name, identification_method,
                                identification_number, postal_address, phone_number, gender, date_of_birth))
                        

            policy_holder = PolicyHolder.objects.filter(individual_user=individual_user).first()
            if not policy_holder:
                if identification_method == 1:
                    policy_holder = PolicyHolder.objects.filter(id_number=identification_number).first()
                    if not policy_holder:
                        policy_holder = PolicyHolder.objects.create(
                            **create_policy_holder(individual_user, first_name, last_name, postal_address, phone_number, 
                            identification_method, identification_number, gender, date_of_birth))
                       
                else:
                    policy_holder = PolicyHolder.objects.filter(
                        passport_number=identification_number).first()
                    if not policy_holder:
                        policy_holder = PolicyHolder.objects.create(
                            **create_policy_holder(individual_user, first_name, last_name, postal_address, phone_number,
                            identification_method, identification_number, gender, date_of_birth)
                        )
                        

            membership = Membership.objects.create(
                **create_membership(user, policy, scheme_group)
            )
            
            print(f"Membership: {membership.id} Created Successfully!!!")

            # create policy payment
            total_premium = pricing_plan.total_premium
            policy_premium = PolicyPremium.objects.create(
                **create_membership_pemium(policy, total_premium, membership)
            )
            print(f"Policy Premium: {policy_premium.id} Created Successfully!!!")
            policy_payment = PolicyPayment.objects.create(
                **create_payment(policy, membership, total_premium)
            )
            print(f"Policy Payment: {policy_payment.id} Created Successfully!!")


            """
            : Membership Configuration 
            : => Used to link Membership to Beneficiaries & Dependents & Cover Levels
            : => If a membership configuration exists, one that does not link to beneficiary, then,
            : ==> Update the existing one, else Create a new one!
            """
            membership_configuration = MembershipConfiguration.objects.filter(membership=membership, beneficiary__isnull=True).first()
            if membership_configuration:
                membership_configuration.cover_level = 50000 #get_pricing_plan_base_cover(pricing_plan.name)
                membership_configuration.save()
            else:
                membership_configuration = MembershipConfiguration.objects.create(membership=membership, cover_level=50000)

            print(f"Membership Config: {membership_configuration.id} Created Successfully!!")


            """
            : Cycle - (Membership Cycle)
            : => A cycle used to track membership status
            : => I already a cycle exists, don't create a new one, 1 membership 1 cycle
            : => => Note that, creation of a cycle triggers creation of a cycle status update instance
            """
            cycle = Cycle.objects.filter(membership=membership).first()
            if not cycle:
                cycle = Cycle.objects.create(
                    membership=membership, 
                    scheme_group=scheme_group, 
                    status="awaiting_payment"
                )
            print(f"Cycle: {cycle.id} Created Successfully!!!")

            member.processed = True 
            member.save()
            print(f"Member: {member.id} Processed Successfully")