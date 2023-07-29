from django.db import connection, transaction
from apps.schemes.models import Scheme, SchemeGroup
from apps.prices.models import PricingPlan, Obligation
from apps.policies.models import Policy, Cycle, CycleStatusUpdates
from apps.users.models import (
    Profile, Membership, MembershipConfiguration, PolicyHolder, User, PolicyHolderRelative
)
from apps.payments.models import PolicyPayment, PolicyPremium
from apps.dependents.models import Beneficiary


from apps.sales.share_data_upload_methods.bulk_upload_methods import get_policy_number_prefix, get_product_id_from_pricing_plan
from apps.sales.main_member_upload_methods.new_members_onboarding_functions import (
    create_policy, create_scheme_group, create_profile, 
    create_policy_holder, create_user, create_membership, create_payment, create_membership_pemium
)
from apps.sales.share_data_upload_methods.member_transition_methods import get_membership_profile, get_membership_policy_holder
from apps.constants.type_checking_methods import check_if_value_is_date
from apps.sales.share_data_upload_methods.date_formatting_methods import date_format_method

class CreditLifePolicyOnboardingMixin(object):
    def __init__(self, seller_details, member_details, policy_details, obligations, beneficiaries):
        self.seller_details = seller_details
        self.member_details = member_details
        self.policy_details = policy_details
        self.obligations = obligations
        self.beneficiaries = beneficiaries


    def run(self):
        self.__onboard_credit_life_policy()

    @transaction.atomic
    def __onboard_credit_life_policy(self):
        seller_details = self.seller_details
        member_details = self.member_details 
        policy_details = self.policy_details 
        obligations = self.obligations 
        beneficiaries = self.beneficiaries 


        scheme = Scheme.objects.get(name="Credit Life")
        pricing_plan = PricingPlan.objects.get(name=policy_details["pricing_plan"])

        """This Is Purposely For Policy Number Construction Only"""
        pricing_plan_name = policy_details["pricing_plan"]
        pricing_product_id = get_product_id_from_pricing_plan(pricing_plan_name)
        pn_data = scheme.get_policy_number("Credit Life")

        print(f"Product ID: {pricing_product_id}, Pricing Plan: {pricing_plan_name}")

        print(f"PN Data: {pn_data}")


        scheme_group = SchemeGroup.objects.create(
            **create_scheme_group(
                scheme=scheme, 
                pricing_plan=pricing_plan, 
                pricing_plan_name=pricing_plan_name
            )
        )
        policy = Policy.objects.create(**create_policy(pn_data))
        scheme_group.policy = policy
        scheme_group.save()

        username = member_details.get("email")
        first_name = member_details.get("first_name")
        last_name = member_details.get("last_name")
        email = member_details.get("email")
        identification_method=member_details.get("identification_method")
        id_number=member_details.get("id_number")
        passport_number=member_details.get("passport_number")
        postal_address=member_details.get("postal_address")
        phone_number=member_details.get("phone_number")
        gender=member_details.get("gender")
        dob=member_details.get("date_of_birth")

        date_of_birth = dob if check_if_value_is_date(dob) == True else date_format_method(dob)

        user = User.objects.create(**create_user(username=username, email=email, first_name=first_name, last_name=last_name))
        user.set_password("test_password")
        user.save()
        

        profile = Profile.objects.create(
            **create_profile(
                user=user, 
                first_name=first_name, 
                last_name=last_name, 
                identification_method=identification_method, 
                id_number=id_number,
                passport_number=passport_number,
                postal_address=postal_address, 
                phone_number=phone_number, 
                gender=gender, 
                date_of_birth=date_of_birth
            )
        ) 

        PolicyHolder.objects.create(
            **create_policy_holder(
                first_name=first_name, 
                last_name=last_name, 
                postal_address=postal_address, 
                phone_number=phone_number, 
                identification_method=identification_method, 
                id_number=id_number, 
                passport_number=passport_number,
                gender=gender, 
                date_of_birth=date_of_birth
            )
        )
        
        membership = Membership.objects.create(
                **create_membership(user, policy, scheme_group)
            )
            
        print(f"Membership: {membership.id} Created Successfully!!!")

        obligations_list = []
        if obligations:
            for x in obligations:
                inception_date = x.get("inception_date")
                i_date = None
                if inception_date:
                    i_date = inception_date if check_if_value_is_date(inception_date) == True else date_format_method(inception_date)
                obligations_list.append(
                    Obligation(
                        profile = profile,
                        policy = policy,
                        membership=membership,
                        credit_reference=x.get("credit_reference"),
                        creditor_name=x.get("creditor_name"),
                        original_balance=x.get("original_balance"),
                        insurance_premium=x.get("insurance_premium"),
                        proposal_installment=x.get("proposal_installment"),
                        inception_date=i_date,
                        obligation_type=x.get("obligation_type"),
                        is_included=x.get("is_included")
                    )
                )
        if obligations_list:
            Obligation.objects.bulk_create(obligations_list)

        obligations_premium = sum(Obligation.objects.filter(profile=profile, policy=policy, membership=membership).filter(is_included=True).values_list("insurance_premium",flat=True))
        amount_insured = sum(Obligation.objects.filter(profile=profile, policy=policy, membership=membership).filter(is_included=True).values_list("original_balance", flat=True))

        policy_premium = PolicyPremium.objects.create(
            **create_membership_pemium(
                policy = policy, 
                total_premium = obligations_premium, 
                membership = membership
            )
        )
        print(f"Policy Premium: {policy_premium.id} Created Successfully!!!")
        PolicyPayment.objects.create(
            **create_payment(policy, membership, obligations_premium)
        )

        beneficiaries_list = []
        if beneficiaries:
            for x in beneficiaries:
                relative_id = None
                relative = PolicyHolderRelative.objects.filter(relative_name__in=[x.get("relationship"), x.get("relationship").capitalize()]).first()
                if relative:
                    relative_id = relative.id
                b_dob_initial = x.get("date_of_birth")
                b_dob = None
                if b_dob_initial:
                    b_dob = b_dob_initial if check_if_value_is_date(b_dob_initial) == True else date_format_method(b_dob_initial)
                beneficiaries_list.append(
                    Beneficiary(
                        membership = membership,
                        schemegroup = scheme_group,
                        policy = policy,
                        relative_id=relative_id,
                        id_number = x.get("id_number"),
                        passport_number = x.get("passport_number"),
                        date_of_birth = b_dob,
                        phone_number = x.get("phone_number"),
                        first_name = x.get("first_name"),
                        last_name = x.get("last_name")
                    )
                )

        if beneficiaries_list:
            Beneficiary.objects.bulk_create(beneficiaries_list)

        membership_configuration = MembershipConfiguration.objects.filter(membership=membership, beneficiary__isnull=True).first()
        if membership_configuration:
            membership_configuration.cover_level = amount_insured #get_pricing_plan_base_cover(pricing_plan.name)
            membership_configuration.save()
        else:
            membership_configuration = MembershipConfiguration.objects.create(membership=membership, cover_level=amount_insured)

        print(f"Membership Config: {membership_configuration.id} Created Successfully!!")

        cycle = Cycle.objects.filter(membership=membership).first()
        if not cycle:
            cycle = Cycle.objects.create(
                membership=membership, 
                scheme_group=scheme_group, 
                status="awaiting_payment"
            )
        print(f"Cycle: {cycle.id} Created Successfully!!!")
