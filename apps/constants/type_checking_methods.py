from datetime import datetime

def check_if_value_is_date(date_value):
    try:
        # Attempt to parse the input string as a date
        datetime.strptime(date_value, "%Y-%m-%d")
        return True
    except ValueError:
        return False