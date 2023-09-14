from datetime import datetime
from decimal import Decimal

current_year = datetime.now().date().year

def get_motor_vehicle_policy_premium(vehicle_price, year_of_manufacture):
    vehicle_premium = 0
    vehicle_age = current_year - int(year_of_manufacture)
    
    if vehicle_age <= 2:
        vehicle_premium = Decimal(0.05) * vehicle_price
    elif vehicle_age >= 3 and vehicle_age <= 5:
        vehicle_premium = Decimal(0.07) * vehicle_price
    elif vehicle_age >= 6 and vehicle_age <= 10:
        vehicle_premium = Decimal(0.09) * vehicle_price
    elif vehicle_age > 10:
        vehicle_premium = Decimal(0.1) * vehicle_price

    return vehicle_premium