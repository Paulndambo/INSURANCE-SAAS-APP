def date_format_method(date_str):
    new_date = date_str.replace("/", "-")
    return new_date[:10]