
def validate_id_number_length(identification_method, identification_number):
    validated_id_number = ""
    identification_number = str(identification_number)
    if identification_method:
        if int(identification_method) == 1:
            if len(identification_number) == 13:
                validated_id_number = identification_number
            elif len(identification_number) == 12:
                validated_id_number = f"0{identification_number}"
            elif len(identification_number) == 11:
                validated_id_number = f"00{identification_number}"
            elif len(identification_number) == 10:
                validated_id_number = f"000{identification_number}"
            elif len(identification_number) == 9:
                validated_id_number = f"0000{identification_number}"
            elif len(identification_number) == 8:
                validated_id_number = f"00000{identification_number}"

        elif int(identification_method) == 0:
            validated_id_number = identification_number

    return validated_id_number


def validate_phone_number_length(phone_number):
    validated_phone_number = ""

    if phone_number:
        phone_number = str(phone_number)
        if len(phone_number) == 9:
            validated_phone_number = f"0{phone_number}"

        return validated_phone_number
    else:
        return None