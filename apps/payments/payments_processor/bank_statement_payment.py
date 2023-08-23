from datetime import datetime, timedelta
from django.db.models import Q

from apps.policies.models import Policy
from apps.payments.models import PolicyPremium, PolicyPayment
from apps.users.models import Profile, Membership

from apps.payments.payments_processor.shared_functions import get_premium_in_range

class BankStatementPaymentProcessMixin(object):
    def __init__(self, data):
        self.data = data

    
    def run(self):
        self.__process_bank_statement()

    
    def __process_bank_statement(self):
        data = self.data

        for bank_statement in data:
            policy_number = bank_statement.get("policy_number")
            amount = bank_statement.get("amount")
            id_number = bank_statement.get("id_number")
            payment_date = bank_statement.get("payment_date")


            profile = Profile.objects.get(id_number=id_number)
            policy = Policy.objects.get(policy_number=policy_number)
            membership = Membership.objects.get(policy=policy, user=profile.user)

           
            policy_premium, passed_date = get_premium_in_range(payment_date, membership)

            if policy_premium:
                if policy_premium.status == "paid":
                    print("*********We could not find an unpaid premium for the customer***********")
                    PolicyPayment.objects.create(
                        policy=policy,
                        amount=amount,
                        payment_date=passed_date,
                        membership=membership,
                        payment_method="manual",
                        state="EARLY PAYMENT"
                    )

                else:
                    premium_status = ''
                    balance = policy_premium.balance + amount
                    if balance == 0 or balance == 0.0:
                        premium_status = 'paid'
                    else:
                        premium_status = 'partial'

                    policy_premium.status = premium_status
                    policy_premium.balance = policy_premium.balance + amount
                    policy_premium.save()
                    
                    PolicyPayment.objects.create(
                        policy=policy,
                        premium=policy_premium,
                        amount=amount,
                        payment_date=passed_date,
                        membership=membership,
                        payment_method="manual",
                        state="SUCCESSFUL"
                    )
                    
            else:
                print("*********We could not find an unpaid premium for the customer***********")
                PolicyPayment.objects.create(
                    policy=policy,
                    amount=amount,
                    payment_date=passed_date,
                    membership=membership,
                    payment_method="manual",
                    state="EARLY PAYMENT"
                )  