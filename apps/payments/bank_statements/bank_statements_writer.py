from apps.payments.models import BankStatement


def write_multiple_bank_statements(data):
    try:
        bank_statements = []
        for x in data:
           
            bank_statements.append(
                BankStatement(
                    policy_number=x.get('policy_number'),
                    statement=x,
                    processed=False
                )
            )

        BankStatement.objects.bulk_create(bank_statements)
    except Exception as e:
        raise e