from apps.entities.models import SalesAgent
from apps.payments.models import PolicyPremium
from apps.pet_insure.models import Pet
from apps.policies.models import Cycle, Policy, PolicyDetails, PolicyHolder
from apps.prices.models import PricingPlan
from apps.sales.main_member_upload_methods.new_members_onboarding_functions import (
    create_membership, create_membership_pemium, create_policy,
    create_policy_holder, create_profile, create_retail_scheme_group,
    create_user)
from apps.schemes.models import Scheme, SchemeGroup
from apps.users.models import (Membership, MembershipConfiguration, Profile,
                               User)


class PetPolicyPurchaseMixin(object):
    def __init__(self, data):
        self.data = data

    def run(self):
        self.__purchase_pet_policy()

    def __purchase_pet_policy(self):
        data = self.data

        scheme = Scheme.objects.get(name="Pet Scheme")

        members = data["members"]
        agent_details = data["agent_details"]
        scheme_group_details = data["scheme_group"]
        policy_details = data["policy_details"]
        quote_details = data["quote_details"]
        pets = data["pets"]

        for member in members:
            identification_number = member.get("id_number")
            date_of_birth = member.get("date_of_birth")
            first_name = member.get("first_name")
            last_name = member.get("last_name")
            postal_address = member.get("postal_address")
            phone_number = member.get("phone_number")
            gender = member.get("gender")
            email = member.get("email")
            username = member.get("email")
            pricing_plan_name = scheme_group_details.get("pricing_plan")
            identification_method = 1


            premium = quote_details.get("premium")
            cover_amount = quote_details.get("cover_amount")

            start_date = policy_details.get("start_date")

            sales_agent_email = agent_details.get("email")
            sales_agent = SalesAgent.objects.filter(user__email=sales_agent_email).first()
            

            pricing_plan = PricingPlan.objects.get(name=pricing_plan_name)

            scheme_group = SchemeGroup.objects.create(
                **create_retail_scheme_group(scheme, pricing_plan, pricing_plan_name, first_name, last_name)
            )

            pn_data = scheme.get_policy_number(pricing_plan_name)
            print(f"PN. Data: {pn_data}")
        
            policy = Policy.objects.create(**create_policy(pn_data, start_date, sales_agent, premium, cover_amount))

            scheme_group.policy = policy
            scheme_group.save()

            PolicyDetails.objects.create(
                policy=policy
            )

            user = User.objects.filter(email=email).first()
            if not user:
                user = User.objects.create(**create_user(username, email, first_name, last_name))
                user.set_password("Password")
                user.save()
            

            profile = Profile.objects.filter(user=user).first()

            if not profile:
                profile = Profile.objects.filter(id_number=identification_number).first()
                if not profile:
                    profile = Profile.objects.create(
                        **create_profile(user, first_name, last_name, identification_method, 
                        identification_number, postal_address, phone_number, gender, date_of_birth)
                    )   
            

            policy_holder = PolicyHolder.objects.filter(id_number=identification_number).first()
            if not policy_holder:
                policy_holder = PolicyHolder.objects.create(
                    **create_policy_holder(user, first_name, last_name, postal_address, 
                    phone_number, identification_method, identification_number, gender, date_of_birth))

                    
            membership = Membership.objects.create(**create_membership(user, policy, scheme_group))
            print(f"Membership: {membership.id} Created Successfully!!!")


            policy_premium = PolicyPremium.objects.create(**create_membership_pemium(policy, premium, membership))
            print(f"Policy Premium: {policy_premium.id} Created Successfully!!!")
            

            membership_configuration = MembershipConfiguration.objects.filter(membership=membership, beneficiary__isnull=True).first()
            if membership_configuration:
                membership_configuration.cover_level = cover_amount
                membership_configuration.save()
            else:
                membership_configuration = MembershipConfiguration.objects.create(
                    membership=membership, cover_level=cover_amount
                )
            print(f"Membership Config: {membership_configuration.id} Created Successfully!!")

            cycle = Cycle.objects.filter(membership=membership).first()

            if not cycle:
                cycle = Cycle.objects.create(
                    membership=membership, scheme_group=scheme_group, status="awaiting_payment"
                )
            print(f"Cycle: {cycle.id} Created Successfully!!!")

            pets_list = []
            for pet in pets:
                pets_list.append(Pet(
                    policy=policy,
                    scheme_group=scheme_group,
                    owner=profile,
                    pet_type = pet.get("pet_type"),
                    name=pet.get("name"),
                    gender=pet.get("gender"),
                    size=pet.get("size"),
                    color=pet.get("color"),
                    description=pet.get("description"),
                    date_of_birth=pet.get("date_of_birth"),
                    breed_id=int(pet.get("breed")),
                ))
            if pets_list:
                Pet.objects.bulk_create(pets_list)

                print("Pets Created Successfully!!")
