from datetime import date
from dateutil.relativedelta import relativedelta

def get_same_date_next_month(expected_date):
    next_month = expected_date + relativedelta(months=1)
    day = expected_date.day

    if next_month.day < day:
        next_month = next_month.replace(day=next_month.day - 1)
    return next_month