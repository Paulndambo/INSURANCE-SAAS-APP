from datetime import datetime

def check_if_value_is_date(date_value):
    try:
        datetime.strptime(date_value, "%Y-%m-%d")
        return True
    except ValueError:
        return False