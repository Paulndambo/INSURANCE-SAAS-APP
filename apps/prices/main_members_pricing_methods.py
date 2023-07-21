from decimal import Decimal

def get_main_member_premium(cover_levels: list, cover_amount):
    premiums = [x for x in cover_levels if Decimal(x["cover_amount"]) == Decimal(cover_amount)]
    premium = 0
    if premiums:
        premium = premiums[0]['premium']
    print(f"Premiums: {premium}")
    return premium


#filtered_students = [student for student in students if student['age'] < 30]
