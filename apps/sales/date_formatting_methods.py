def date_format_method(date_str):
    if date_str:
        new_date = date_str.replace("/", "-")
        return new_date[:10]
    else:
        return None