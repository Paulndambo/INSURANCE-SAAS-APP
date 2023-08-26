from datetime import datetime

from apps.constants.premium_methods import get_same_date_next_month
from apps.payments.models import PolicyPremium

date_today = datetime.now().date()

def raise_new_policy_premium(membership):
    latest_premium = membership.membershipprems.order_by("-expected_date").first()

    next_expected_date = get_same_date_next_month(latest_premium.expected_date)
    next_premium_amount = latest_premium.expected_payment
    next_balance = -abs(latest_premium.balance - next_premium_amount)

    new_premium = membership.membershipprems.create(
        policy=latest_premium.policy,
        membership=latest_premium.membership,
        amount_paid=0,
        expected_payment=next_premium_amount,
        expected_date=next_expected_date,
        balance=next_balance,
        status="future"
    )


    print(f"Premium: {new_premium.id} Expected On: {new_premium.expected_date} Created Successfully!!")


def raise_new_premiums():
    try:
        premiums = PolicyPremium.objects.filter(expected_date=date_today)
        for premium in premiums:
            latest_premium = premium.membership.membershipprems.order_by("-expected_date").first()

            if latest_premium.expected_date > date_today:
                print(f"Membership: {latest_premium.membership.id} Already has a future premium!")
            else:
                premium.membership.raise_new_policy_premium()
                print(f"Prem. ID: {premium.id}, Expected Date: {premium.expected_date}, Status: {premium.status}")
    except Exception as e:
        raise e
    