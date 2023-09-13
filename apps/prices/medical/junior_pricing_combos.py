HOSPITALS = ["Unlimited", "Getrude"]

INPATIENT_COVER_LEVELS = [
    {"cover": 500000, "premium": 150}, 
    {"cover": 1000000, "premium": 200}, 
    {"cover": 3000000, "premium": 250}, 
    {"cover": 5000000, "premium": 300}
]
OUTPATIENT_COVER_LEVELS = [50000]

hospital = "Getrude"
inpatient_cover = 0
outpatient_cover = 0

def calculate_junior_cover_premium(hospital, inpatient_cover, outpatient_cover):
    child_premium = 0
    if hospital == "Getrude":
        if inpatient_cover == 500000 and outpatient_cover == 50000:
            child_premium = 100
        
        elif inpatient_cover == 1000000 and outpatient_cover == 50000:
            child_premium = 150

        elif inpatient_cover == 2000000 and outpatient_cover == 50000:
            child_premium = 200

        elif inpatient_cover == 3000000 and outpatient_cover == 50000:
            child_premium = 300

        elif inpatient_cover == 5000000 and outpatient_cover == 50000:
            child_premium = 350

    elif hospital == "Unlimited":
        if inpatient_cover == 500000 and outpatient_cover == 50000:
            child_premium = 150
        
        elif inpatient_cover == 1000000 and outpatient_cover == 50000:
            child_premium = 200

        elif inpatient_cover == 2000000 and outpatient_cover == 50000:
            child_premium = 250

        elif inpatient_cover == 3000000 and outpatient_cover == 50000:
            child_premium = 350

        elif inpatient_cover == 5000000 and outpatient_cover == 50000:
            child_premium = 400
            
    return child_premium