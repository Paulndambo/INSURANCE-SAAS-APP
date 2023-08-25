import functools
extended_dependents = [
        {
            "first_name": "Grandpa",
            "add_on_premium": 30,
            
        },
        {
            "first_name": "Grandma",
            "add_on_premium": 240,
        },
        {
            "first_name": "Auntie",
            "add_on_premium": 40,
        
        }
    ]

total_add_on_prem = sum([x['add_on_premium'] for x in extended_dependents])
x = functools.reduce(lambda x, y: x['add_on_premium'] + y['add_on_premium'], extended_dependents)
print(x)
