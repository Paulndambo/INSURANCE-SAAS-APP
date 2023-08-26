from datetime import datetime, timedelta
from django.db.models import Q

from apps.policies.models import Policy
from apps.payments.models import PolicyPremium, PolicyPayment
from apps.users.models import Profile, Membership
from apps.payments.payments_processor.shared_functions import get_premium_in_range


date_today = datetime.now().date()


class ManualPaymentProcessingMixin(object):
    def __init__(self, data):
        self.data = data


    def run(self):
        self.__process_manual_payment()
        

    def __process_manual_payment(self):
        try: 
            data = self.data

            policy_number = data.get("policy_number")
            amount = data.get("amount")
            payment_date = data.get("payment_date")
            premium = data.get("premium")
            id_number = data.get("id_number")

            passed_date = datetime.strptime(payment_date, '%Y-%m-%d') if payment_date else date_today
            first_day = passed_date.replace(day=1)
            last_day = first_day.replace(month=first_day.month % 12 + 1, day=1) - timedelta(days=1)

            profile = Profile.objects.get(id_number=id_number)
            policy = Policy.objects.get(policy_number=policy_number)
            membership = Membership.objects.get(policy=policy, user=profile.user)


            policy_premium = None

            if premium:
                policy_premium = PolicyPremium.objects.get(id=premium)

                print("Premium Found using premium ID")
            else:
                premium_record_1 = PolicyPremium.objects.filter(
                    Q(expected_date__range=(first_day, last_day)) & Q(membership=membership), status__in=['future', 'unpaid', 'pending']
                ).first()

                premium_record_2 = PolicyPremium.objects.filter(
                        membership=membership, status__in=['future', 'unpaid', 'pending']
                    ).order_by("-expected_date").first()

                policy_premium = premium_record_1 if premium_record_1 else premium_record_2

                
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
                    policy_premium.amount_paid += amount
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
        except Exception as e:
            raise e