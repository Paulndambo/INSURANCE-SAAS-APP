def get_spouse_premium(inpatient_cover, outpatient_cover, age_group):
    spouse_premium = 0

    if age_group == "19-29" and inpatient_cover == 500000 and outpatient_cover == 50000:
        spouse_premium = 500

    if age_group == "30-40" and inpatient_cover == 500000 and outpatient_cover == 60000:
        spouse_premium = 500
    if age_group == "41-50" and inpatient_cover == 500000 and outpatient_cover == 100000:
        spouse_premium = 500

    if age_group == "51-65" and inpatient_cover == 500000 and outpatient_cover == 50000:
        spouse_premium = 500

age_group, outpatient_cover, inpatient_cover, premium
19-29, 500000, 50000, 500
19-29, 500000, 60000, 550
19-29, 500000, 70000, 600
19-29, 500000, 100000, 650
19-29, 500000, 150000, 700
19-29, 500000, 200000, 750

30-40, 500000, 50000, 500
30-40, 500000, 60000, 550
30-40, 500000, 70000, 600
30-40, 500000, 100000, 650
30-40, 500000, 150000, 700
30-40, 500000, 200000, 750

41-50, 500000, 50000, 500
41-50, 500000, 60000, 550
41-50, 500000, 70000, 600
41-50, 500000, 100000, 650
41-50, 500000, 150000, 700
41-50, 500000, 200000, 750