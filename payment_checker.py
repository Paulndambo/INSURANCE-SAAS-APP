def calculate_divisions(amount_paid, debt_amount):
    divisions = []

    if amount_paid > debt_amount:
        multiple_factor = amount_paid // debt_amount
        remainder = amount_paid % debt_amount

        for i in range(multiple_factor):
            divisions.append({"id": i + 1, "division_amount": debt_amount})
        
        if remainder > 0:
            divisions.append({"id": multiple_factor + 1, "division_amount": remainder})
    
    return divisions

# Example usage
amount_paid = 750
debt_amount = 300

result = calculate_divisions(amount_paid, debt_amount)
print(result)
