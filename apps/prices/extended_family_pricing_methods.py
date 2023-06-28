def get_synergy_extended_premium(age, cover_level):
    level_premium = 0

    if cover_level == 15000:
        if age >= 75:
            level_premium = 240
        elif age >= 60 and age <= 74:
            level_premium = 120
        elif age >= 40 and age <= 59:
            level_premium = 50
        elif age >= 22 and age <= 39:
            level_premium = 30

    elif cover_level == 10000:
        if age >= 75:
            level_premium = 170
        elif age >= 60 and age <= 74:
            level_premium = 70
        elif age >= 40 and age <= 59:
            level_premium = 40
        elif age >= 22 and age <= 39:
            level_premium = 20

    return level_premium


def get_legacy_extended_premium(age, cover_level):
    level_premium = 0

    if cover_level == 20000:
        if age >= 75:
            level_premium = 182.15
        elif age >= 65 and age <= 74:
            level_premium = 78.01
        elif age >= 0 and age <= 64:
            level_premium = 25.94

    elif cover_level == 15000:
        if age >= 75:
            level_premium = 136.67
        elif age >= 65 and age <= 74:
            level_premium = 58.46
        elif age >= 0 and age <= 64:
            level_premium = 19.55

    elif cover_level == 10000:
        if age >= 75:
            level_premium = 90.97
        elif age >= 65 and age <= 74:
            level_premium = 39.10
        elif age >= 0 and age <= 64:
            level_premium = 12.98

    return level_premium


def get_non_legacy_extended_premium(age, cover_level):
    level_premium = 0

    return level_premium
