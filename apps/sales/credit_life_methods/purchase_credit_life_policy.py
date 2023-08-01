from django.db import connection, transaction
from apps.schemes.models import Scheme, SchemeGroup
from apps.prices.models import PricingPlan, Obligation
from apps.policies.models import Policy, Cycle, CycleStatusUpdates
from apps.users.models import (
    Profile, Membership, MembershipConfiguration, PolicyHolder, User, PolicyHolderRelative
)
from apps.payments.models import PolicyPayment, PolicyPremium
from apps.dependents.models import Beneficiary
from apps.entities.models import SalesAgent


from apps.sales.share_data_upload_methods.bulk_upload_methods import get_policy_number_prefix, get_product_id_from_pricing_plan
from apps.sales.main_member_upload_methods.new_members_onboarding_functions import (
    create_policy, create_retail_scheme_group, create_profile, 
    create_policy_holder, create_user, create_membership, create_payment, create_membership_pemium
)
from apps.sales.share_data_upload_methods.member_transition_methods import get_membership_profile, get_membership_policy_holder
from apps.constants.type_checking_methods import check_if_value_is_date
from apps.sales.share_data_upload_methods.date_formatting_methods import date_format_method

class CreditLifePolicyOnboardingMixin(object):
    def __init__(self, data):
        self.data = data
        

    def run(self):
        self.__onboard_credit_life_policy()


    @transaction.atomic
    def __onboard_credit_life_policy(self):
        data = self.data

        scheme = Scheme.objects.get(scheme_type="credit")

        agent_details = data["agent_details"]
        members = data["members"]
        policy_details = data["policy_details"] 
        obligations = data["obligations"] 
        beneficiaries = data["beneficiaries"] 
        scheme_group_details = data["scheme_group"]
        quote_details = data["quote_details"]

        for member in members:
            scheme = Scheme.objects.get(scheme_type="credit")
            pricing_plan_name = scheme_group_details.get("pricing_plan")
            pricing_plan = PricingPlan.objects.filter(name=pricing_plan_name).first()


            identification_number = member.get("id_number")
            date_of_birth = member.get("date_of_birth")
            first_name = member.get("first_name")
            last_name = member.get("last_name")
            postal_address = member.get("postal_address")
            phone_number = member.get("phone_number")
            gender = member.get("gender")
            email = member.get("email")
            username = member.get("email")
            identification_method = 1

            premium = quote_details.get("premium")
            cover_amount = quote_details.get("cover_amount")

            sales_agent_email = agent_details.get("email")
            sales_agent = SalesAgent.objects.filter(user__email=sales_agent_email).first()
            start_date = policy_details.get("start_date")
            
            
            scheme_group = SchemeGroup.objects.create(**create_retail_scheme_group(scheme, pricing_plan, pricing_plan_name, first_name, last_name))

            pn_data = scheme.get_policy_number(pricing_plan_name)
            print(f"PN Data: {pn_data}")
            policy = Policy.objects.create(**create_policy(pn_data, start_date, sales_agent, premium, cover_amount))
            scheme_group.policy = policy
            scheme_group.save()


            user = User.objects.create(**create_user(username=username, email=email, first_name=first_name, last_name=last_name))
            user.set_password("test_password")
            user.save()
            

            profile = Profile.objects.create(
                **create_profile(
                    user=user, 
                    first_name=first_name, 
                    last_name=last_name, 
                    identification_method=identification_method, 
                    id_number=identification_number,
                    postal_address=postal_address, 
                    phone_number=phone_number, 
                    gender=gender, 
                    date_of_birth=date_of_birth
                )
            ) 

            PolicyHolder.objects.create(
                **create_policy_holder(
                    user=user,
                    first_name=first_name, 
                    last_name=last_name, 
                    postal_address=postal_address, 
                    phone_number=phone_number, 
                    identification_method=identification_method, 
                    id_number=identification_number, 
                    gender=gender, 
                    date_of_birth=date_of_birth
                )
            )
            
            membership = Membership.objects.create(**create_membership(user, policy, scheme_group))
            print(f"Membership: {membership.id} Created Successfully!!!")

            obligations_list = []
            if obligations:
                for x in obligations:
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
                            inception_date=x.get("inception_date"),
                            obligation_type=x.get("obligation_type"),
                            is_included= True if x.get("is_included") == "included" else False
                        )
                    )
            if obligations_list:
                Obligation.objects.bulk_create(obligations_list)

           
            policy_premium = PolicyPremium.objects.create(
                **create_membership_pemium(
                    policy = policy, 
                    total_premium = premium, 
                    membership = membership
                )
            )
            print(f"Policy Premium: {policy_premium.id} Created Successfully!!!")
            PolicyPayment.objects.create(**create_payment(policy, membership, premium))

            beneficiaries_list = []
            if beneficiaries:
                for x in beneficiaries:
                    relative = PolicyHolderRelative.objects.get(relative_name="Beneficiary")
                
                    beneficiaries_list.append(
                        Beneficiary(
                            membership = membership,
                            schemegroup = scheme_group,
                            policy = policy,
                            relative=relative,
                            relationship=x.get("relationship"),
                            id_number = x.get("id_number"),
                            date_of_birth = x.get("date_of_birth"),
                            phone_number = x.get("phone_number"),
                            first_name = x.get("first_name"),
                            last_name = x.get("last_name")
                        )
                    )

            if beneficiaries_list:
                Beneficiary.objects.bulk_create(beneficiaries_list)

            membership_configuration = MembershipConfiguration.objects.filter(membership=membership, beneficiary__isnull=True).first()
            if membership_configuration:
                membership_configuration.cover_level = cover_amount #get_pricing_plan_base_cover(pricing_plan.name)
                membership_configuration.save()
            else:
                membership_configuration = MembershipConfiguration.objects.create(membership=membership, cover_level=cover_amount)

            print(f"Membership Config: {membership_configuration.id} Created Successfully!!")

            cycle = Cycle.objects.filter(membership=membership).first()
            if not cycle:
                cycle = Cycle.objects.create(
                    membership=membership, 
                    scheme_group=scheme_group, 
                    status="awaiting_payment"
                )
            print(f"Cycle: {cycle.id} Created Successfully!!!")
