from apps.payments.models import BankStatement, PaymentLog, PolicyPayment
from apps.payments.shared_functions import get_premium_in_range
from apps.policies.models import Policy
from apps.users.models import Membership, Profile


class BankStatementPaymentProcessMixin(object):
    
    def __init__(self, data):
        self.data = data

    
    def run(self):
        self.__process_bank_statement()

    
    def __process_bank_statement(self):
        data = self.data

        bank_statements_list = []
        for bank_statement in data:
            policy_number = bank_statement.get("policy_number")
            amount = bank_statement.get("amount")
            id_number = bank_statement.get("id_number")
            payment_date = bank_statement.get("payment_date")

            profile = Profile.objects.filter(id_number=id_number).first()
            
            policy = Policy.objects.filter(policy_number=policy_number).first()

            membership = None
            if profile:
                membership = Membership.objects.filter(policy=policy, user=profile.user).first()

            
            bank_statements_list.append(PaymentLog(
                id_number=id_number,
                policy=policy,
                membership=membership,
                amount=amount,
                processed=False,
                payment_date=payment_date,
                payment_type="bank_statement",
                balance=amount
            ))
  
               
            bank_statement = BankStatement.objects.create(
                policy_number=policy_number,
                statement=bank_statement,
                processed=False
            )
        
        PaymentLog.objects.bulk_create(bank_statements_list)
            