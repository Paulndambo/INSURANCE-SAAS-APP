from apps.sales.date_formatting_methods import date_format_method
def new_member_data_constructor(data):
    new_object = {
        "username": data.get("username"),
        "firstname": data.get("firstname", "first name"),
        "lastname": data.get("lastname", "last name"),
        "email": data.get("email"),
        "identification_method": data.get("identification method", "identification_method"),
        "identification_number": data.get("identification number", "identification_number"),
        "mobile_number": data.get("mobile number", "mobile_number"),
        "landline": data.get("landline"),
        "date_of_birth": date_format_method(data.get("date of birth", "date_of_birth")),
        "physical_address": data.get("physical address", "physical_address"),
        "postal_address": data.get("postal address", "postal_address"),
        "gender": data.get("gender"),
        "product": data.get("product")
    }

    return new_object