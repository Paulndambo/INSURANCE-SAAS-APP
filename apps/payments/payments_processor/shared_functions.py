from datetime import datetime, timedelta
from django.db.models import Q
from apps.payments.models import PolicyPremium

date_today = datetime.now().date()

def get_premium_in_range(payment_date, membership):
    passed_date = datetime.strptime(payment_date, '%Y-%m-%d') if payment_date else date_today
    first_day = passed_date.replace(day=1)
    last_day = first_day.replace(month=first_day.month % 12 + 1, day=1) - timedelta(days=1)

    policy_premium = None


    premium_record_1 = PolicyPremium.objects.filter(
        Q(expected_date__range=(first_day, last_day)) & Q(membership=membership), status__in=['future', 'unpaid', 'pending']
    ).first()

    premium_record_2 = PolicyPremium.objects.filter(
            membership=membership, status__in=['future', 'unpaid', 'pending']
        ).order_by("-expected_date").first()

    policy_premium = premium_record_1 if premium_record_1 else premium_record_2

    return policy_premium, passed_date

