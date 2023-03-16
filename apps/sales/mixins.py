from apps.sales.queries import query
from django.db import connection, transaction
from datetime import datetime, date

from apps.sales.bulk_upload_methods import (
    get_policy_number_prefix,
    get_premium_amount,
    get_pricing_plan,
    get_product_id_from_pricing_plan,
    validate_id_number_length,
    validate_phone_number_length,
    
)
from apps.sales.date_formatting_methods import date_format_method
from apps.sales.mark_members_as_paid import mark_members_as_paid
from apps.sales.get_membership import get_membership


##Apps Imports
from apps.schemes.models import Scheme, SchemeGroup
from apps.policies.models import (
    Policy,
    PolicyCancellation,
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
from apps.sales.models import PricingPlanSchemeMapping

from apps.dependents.models import Dependent, Beneficiary


class BulkMembersOnboardingMixin(object):
    def __init__(self, data):
        self.data = data

    def run(self):
        self.__onboard_members()

    @transaction.atomic
    def __onboard_members(self):
        group_plans = list(PricingPlanSchemeMapping.objects.filter(scheme_type="group").values_list("name", flat=True))
        retail_plans = list(PricingPlanSchemeMapping.objects.filter(scheme_type="retail").values_list("name", flat=True))

        first_member = self.data.upload_data[0]
        pricing_plan = PricingPlan.objects.get(name=get_pricing_plan(first_member["product"]))

        pricing_plan_name = pricing_plan.name

        print(pricing_plan_name)
        #print(group_plans)

        
        if pricing_plan_name in retail_plans:
            bulk_retail_mixin = BulkRetailMemberOnboardingMixin(self.data)
            bulk_retail_mixin.run()

        elif pricing_plan_name in group_plans:
            bulk_group_mixin = BulkGroupMembersOnboardingMixin(self.data)
            bulk_group_mixin.run()
        


class BulkGroupMembersOnboardingMixin(object):
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

        last_policy = Policy.objects.last()

        pricing_plan = PricingPlan.objects.get(name=get_pricing_plan(first_member["product"]))
        scheme = Scheme.objects.get(name="Group Scheme")

        scheme_group = SchemeGroup.objects.create(
            scheme_id=scheme.id,
            name=get_pricing_plan(first_member["product"]),
            payment_method="off_platform",
            period_type="monthly",
            period_frequency=1,
            pricing_group=pricing_plan,
            cycle_type="member",
            description=get_pricing_plan(first_member["product"]),
        )

        policy = Policy.objects.create(
            policy_number=f"{get_policy_number_prefix(first_member['product'])}{last_policy.id+1}",
            start_date=datetime.now(),
            payment_day=2,
            status="created",
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
                    "role": "individual",
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
                if data["identification method"] == 1:

                    profile = Profile.objects.filter(id_number=data["identification number"]).first()

                    if not profile:
                        profile = Profile.objects.create(
                            user=user,
                            first_name=data["firstname"],
                            last_name=data["lastname"],
                            id_number=data["identification number"],
                            physical_address=data["postal address"],
                            postal_address=data["postal address"],
                            phone_number=data["mobile number"],
                            work_phone_number=data["mobile number"],
                            home_phone_number=data["landline"],
                            gender=data["gender"],
                            date_of_birth= date_format_method(data["date of birth"])
                        )
                        profile.save()
                else:
                    profile = Profile.objects.filter(passport_number=data["identification number"]).first()
                    if not profile:
                        profile = Profile.objects.create(
                            user=user,
                            first_name=data["firstname"],
                            last_name=data["lastname"],
                            passport_number=data["identification number"],
                            physical_address=data["postal address"],
                            postal_address=data["postal address"],
                            phone_number=data["mobile number"],
                            work_phone_number=data["mobile number"],
                            home_phone_number=data["landline"],
                            gender=data["gender"],
                            date_of_birth=date_format_method(
                                data["date of birth"])
                        )
                        profile.save()

            policy_holder = PolicyHolder.objects.filter(user=user).first()

            if not policy_holder:
                if data["identification method"] == 1:
                    policy_holder = PolicyHolder.objects.create(
                        user=user,
                        postal_address=data["postal address"],
                        phone_number=data["mobile number"],
                        id_number=data["identification number"],
                        gender=data["gender"],
                        date_of_birth=date_format_method(data["date of birth"])
                    )
                    policy_holder.save()
                else:
                    policy_holder = PolicyHolder.objects.create(
                        user=user,
                        postal_address=data["postal address"],
                        passport_number=data["identification number"],
                        gender=data["gender"],
                        ddate_of_birth=date_format_method(data["date of birth"]),
                        phone_number=data["mobile number"],
                    )
                    policy_holder.save()


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
                membership=membership, cover_level=50000, pricing_plan=pricing_plan
            )
            membership_configuration.save()

            print(
                f"Membership Config: {membership_configuration.id} Created Successfully!!"
            )

            cycle = Cycle.objects.filter(membership=membership).first()

            if not cycle:
                cycle = Cycle.objects.create(
                    membership=membership, scheme_group=scheme_group, status="active"
                )

            print(f"Cycle: {cycle.id} Created Successfully!!!")

            CycleStatusUpdates.objects.create(cycle=cycle, previous_status="awaiting_payment", next_status="active")
            print("****************End of Member Onboarding****************")



class BulkRetailMemberOnboardingMixin(object):
    def __init__(self, data):
        self.data = data


    def run(self):
        self.__onboard_retail_members()

    def __onboard_retail_members(self):
        members = self.data

        scheme = Scheme.objects.get(name="Retail Scheme")
        
        for data in members.upload_data:
            pricing_plan = PricingPlan.objects.get(name=get_pricing_plan(data["product"]))

            scheme_group = SchemeGroup.objects.create(
                scheme_id=scheme.id,
                name=get_pricing_plan(data["product"]),
                payment_method="debit_order",
                period_type="monthly",
                period_frequency=1,
                pricing_group=pricing_plan,
                cycle_type="member",
                description=get_pricing_plan(data["product"]),
            )

            last_policy = Policy.objects.last()

            policy = Policy.objects.create(
                policy_number=f"{get_policy_number_prefix(data['product'])}{last_policy.id+1}",
                start_date=datetime.now(),
                payment_day=2,
                status="created",
                dg_required=False,
            )

            scheme_group.policy = policy
            scheme_group.save()

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
                    "role": "individual",
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
                if data["identification method"] == 1:

                    profile = Profile.objects.filter(id_number=data["identification number"]).first()

                    if not profile:
                        profile = Profile.objects.create(
                            user=user,
                            first_name=data["firstname"],
                            last_name=data["lastname"],
                            id_number=data["identification number"],
                            physical_address=data["postal address"],
                            postal_address=data["postal address"],
                            phone_number=data["mobile number"],
                            work_phone_number=data["mobile number"],
                            home_phone_number=data["landline"],
                            gender=data["gender"],
                            date_of_birth=date_format_method(
                                data["date of birth"])
                        )
                        profile.save()
                else:
                    profile = Profile.objects.filter(
                        passport_number=data["identification number"]).first()
                    if not profile:
                        profile = Profile.objects.create(
                            user=user,
                            first_name=data["firstname"],
                            last_name=data["lastname"],
                            passport_number=data["identification number"],
                            physical_address=data["postal address"],
                            postal_address=data["postal address"],
                            phone_number=data["mobile number"],
                            work_phone_number=data["mobile number"],
                            home_phone_number=data["landline"],
                            gender=data["gender"],
                            date_of_birth=date_format_method(
                                data["date of birth"])
                        )
                        profile.save()

            policy_holder = PolicyHolder.objects.filter(user=user).first()

            if not policy_holder:
                if data["identification method"] == 1:
                    policy_holder = PolicyHolder.objects.create(
                        user=user,
                        postal_address=data["postal address"],
                        phone_number=data["mobile number"],
                        id_number=data["identification number"],
                        gender=data["gender"],
                        date_of_birth=date_format_method(data["date of birth"])
                    )
                    policy_holder.save()
                else:
                    policy_holder = PolicyHolder.objects.create(
                        user=user,
                        postal_address=data["postal address"],
                        passport_number=data["identification number"],
                        gender=data["gender"],
                        ddate_of_birth=date_format_method(
                            data["date of birth"]),
                        phone_number=data["mobile number"],
                    )
                    policy_holder.save()

            membership = Membership.objects.create(
                user=user,
                scheme_group=scheme_group,
                policy=policy,
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

            print(f"Policy Premium: {policy_premium.id} Created Successfully!!!")

            policy_payment = PolicyPayment.objects.create(
                policy=policy,
                membership=membership,
                premium=total_premium,
                payment_due_date=datetime.now().date(),
            )

            print(f"Policy Payment: {policy_payment.id} Created Successfully!!")

            membership_configuration = MembershipConfiguration.objects.create(
                membership=membership, cover_level=50000, pricing_plan=pricing_plan
            )
            membership_configuration.save()

            print(f"Membership Config: {membership_configuration.id} Created Successfully!!")

            cycle = Cycle.objects.filter(membership=membership).first()

            if not cycle:
                cycle = Cycle.objects.create(
                    membership=membership, scheme_group=scheme_group, status="active"
                )

            print(f"Cycle: {cycle.id} Created Successfully!!!")

            CycleStatusUpdates.objects.create(
                cycle=cycle, previous_status="awaiting_payment", next_status="active"
            )
            print("****************End of Member Onboarding****************")



class BulkPaidMembersMixin(object):
    def __init__(self, data):
        self.data = data 


    def run(self):
        self.__mark_members_as_paid()


    def __mark_members_as_paid(self):
        for member in self.data:
            try:
                mark_members_as_paid(
                    member['identification method'], 
                    member['identification number'],
                    member['product']
                )
            except Exception as e:
                raise e


class FamilyMembersOnboardingMixin(object):
    def __init__(self, data):
        self.data = data


    def run(self):
        self.__onboard_family_members()


    def __onboard_family_members(self):
        dependents_types = ["Dependant", "Dependent"]
        for x in self.data:
            if x.relationship_type.lower() in [x.lower() for x in dependents_types]:
                dependent_mixin = DependentOnboardingMixin(x)
                dependent_mixin.run()
            elif x.relationship_type.lower() == "Beneficiary".lower():
                beneficiary_mixin = BeneficiaryOnboardingMixin(x)
                beneficiary_mixin.run()
            elif x.relationship_type.lower() == "Extended".lower():
                extended_mixin = ExtendedFamilyMembersOnboardingMixin(x)
                extended_mixin.run()
            else:
                raise ValueError("The Relationship Type You Passed Can't Be Processed!!!!!!")


class DependentOnboardingMixin(object):
    def __init__(self, data):
        self.data = data

    def run(self):
        self.__onboard_dependents()


    def __onboard_dependents(self):
        data = self.data
        membership = get_membership(
            data['main_member_identification_number'],
            data['identification_method'],
            int(data['product'])
        )

        if membership:
            dependent = Dependent(
                membership=membership,
                is_additional_family_member=False,
                
            )


class ExtendedFamilyMembersOnboardingMixin(object):
    def __init__(self, data):
        self.data = data


    def run(self):
        pass

    def __onboard_extended_family_members(self):
        pass


class BeneficiaryOnboardingMixin(object):
    def __init__(self, data):
        self.data = data 

    def run(self):
        pass

    def __onboard_beneficiaries(self):
        pass
