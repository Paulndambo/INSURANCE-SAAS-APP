from apps.sales.date_formatting_methods import date_format_method
from apps.sales.bulk_upload_methods import validate_id_number_length, validate_phone_number_length


def get_cover_level_value(data):
    cover_level = 0
    value = data.get("cover level") if data.get(
        "cover level") else data.get("cover_level")
    if value:
        cover_level = value

    return cover_level

def new_member_data_constructor(data):
    identification_method = data.get("identification method") if data.get("identification method") else data.get("identification_method")
    identification_number = data.get("identification number") if data.get("identification number") else data.get("identification_number")
    mobile_number = data.get("mobile number") if data.get("mobile number") else data.get("mobile_number")

    new_object = {
        "username": data.get("username"),
        "firstname": data.get("firstname") if data.get("firstname") else data.get("first_name"),
        "lastname": data.get("lastname") if data.get("lastname") else data.get("last_name"),
        "email": data.get("email"),
        "identification_method": identification_method,
        "identification_number": validate_id_number_length(identification_method, identification_number),
        "mobile_number": validate_phone_number_length(mobile_number),
        "landline": data.get("landline"),
        "date_of_birth": date_format_method(data.get("date of birth") if data.get("date of birth") else data.get("date_of_birth")),
        "physical_address": data.get("physical address") if data.get("physical address") else data.get("physical_address"),
        "postal_address": data.get("postal address") if data.get("postal address") else data.get("postal_address"),
        "gender": data.get("gender"),
        "product": data.get("product"),
        "cover_level": get_cover_level_value(data),
        "premium": data.get("premium", 0)
    }

    return new_object



def telesales_new_member_data_constructor(data):
    identification_method = data.get("identification method") if data.get( "identification method") else data.get("identification_method")
    identification_number = data.get("identification number") if data.get("identification number") else data.get("identification_number")
    mobile_number = data.get("mobile number") if data.get("mobile number") else data.get("mobile_number")
    new_object = {
        "username": data.get("username"),
        "firstname": data.get("firstname") if data.get("firstname") else data.get("first_name"),
        "lastname": data.get("lastname") if data.get("lastname") else data.get("last_name"),
        "email": data.get("email"),
        "identification_method": data.get("identification method") if data.get("identification method") else data.get("identification_method"),
        "identification_number": validate_id_number_length(identification_method, identification_number),
        "mobile_number": validate_phone_number_length(mobile_number),
        "landline": data.get("landline"),
        "date_of_birth": date_format_method(data.get("date of birth") if data.get("date of birth") else data.get("date_of_birth")),
        "physical_address": data.get("physical address") if data.get("physical address") else data.get("physical_address"),
        "postal_address": data.get("postal address") if data.get("postal address") else data.get("postal_address"),
        "gender": data.get("gender"),
        "product": data.get("product"),
        "cover_level": get_cover_level_value(data),
        "premium": data.get("premium", 0)
    }

    return new_object
