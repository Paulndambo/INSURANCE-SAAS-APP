from datetime import datetime

def calculate_age(date_of_birth):
    if date_of_birth:
        date_today = datetime.utcnow().date()
        birthday = datetime.strptime(date_of_birth, '%Y-%m-%d')

        years = date_today.year - birthday.year - \
            ((date_today.month, date_today.day) < (birthday.month, birthday.day))
        return years
    return None



def check_date_separator(date_str):
    date_separator = ""
    if "/" in date_str:
        date_separator = "/"
    elif "-" in date_str:
        date_separator = "-"

    return date_separator


def date_format_method(date_str):
    if date_str:
        date_separator = check_date_separator(date_str)
        if date_separator == "/":
            new_date = date_str.replace("/", "-")
            return new_date[:10]
        elif date_separator == "-":
            new_date = date_str
            return new_date
        else:
            return None
    return None