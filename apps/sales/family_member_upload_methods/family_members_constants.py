child_types = ['Son', 'Daughter', 'Child']
parent_in_law_types = ['Parent In-Law', 'Parent in law']
mother_in_law_types = ['Mother in law', 'mother_in_law', 'Mother-in-law', 'Mother-In-Law', 'Mother_In_Law', 'Mother In-Law']
father_in_law_types = ['Father in law', 'father_in_law', 'Father-in-law', 'Father-In-Law', 'Father_In_Law', 'Father In-Law']
sibling_in_laws_types = ['Sibling In-Law', 'Sibling in law']
sister_in_law_types = ['Sister in law', 'Sister In-Law', 'Sister_in_law', 'Sister-in-law']
brother_in_law_types = ['Brother in law', 'Brother In-Law', 'Brother_in_law', 'Brother-in-law']
son_in_law_types = ['Son in law', 'Son In-Law', 'Son-in-law', 'Son_in_law']
daughter_in_law_types = ['Daughter in law', 'Daughter In-Law', 'Daughter-in-law', 'Daughter_in_law']
adult_child_types = ["Adult Child", "Adult-Child", "Adult_child"]
minor_child_types = ["Minor Child", "Minor-Child", "Minor_child"]

grandparent_types = ['Grandparent', 'Grandfather', 'Grandmother']
grandchildren_types = ['Grandchild', 'Granddaughter', 'Grandson']
sibling_types = ['Sibling', 'Brother', 'Sister']
cousin_types = ['Cousin', 'cousin', 'COUSIN']
spouse_types = ['Spouse', 'Partner', 'Wife', 'Husband']
father_types = ['Father', 'Step father', 'Step-Father']
mother_types = ['Mother', 'Step Mother', 'Step-Mother']


def get_relationship_types(relationship: str):
    relationship_result = ''
    if relationship.lower() in [x.lower() for x in child_types]:
        relationship_result = 'child'
    elif relationship.lower() in [x.lower() for x in spouse_types]:
        relationship_result = 'spouse'
    elif relationship.lower() in [x.lower() for x in father_types]:
        relationship_result = 'father'
    elif relationship.lower() in [x.lower() for x in mother_types]:
        relationship_result = 'mother'
    elif relationship.lower() in [x.lower() for x in grandparent_types]:
        relationship_result = 'grandparent'
    elif relationship.lower() in [x.lower() for x in grandchildren_types]:
        relationship_result = 'grandchild'
    elif relationship.lower() in [x.lower() for x in mother_in_law_types]:
        relationship_result = 'mother_in_law'
    elif relationship.lower() in [x.lower() for x in father_in_law_types]:
        relationship_result = 'father_in_law'
    elif relationship.lower() in [x.lower() for x in sister_in_law_types]:
        relationship_result = 'sister_in_law'
    elif relationship.lower() in [x.lower() for x in brother_in_law_types]:
        relationship_result = 'brother_in_law'
    elif relationship.lower() in [x.lower() for x in son_in_law_types]:
        relationship_result = 'son_in_law'
    elif relationship.lower() in [x.lower() for x in daughter_in_law_types]:
        relationship_result = 'daughter_in_law'
    elif relationship.lower() in [x.lower() for x in parent_in_law_types]:
        relationship_result = 'parent_in_law'
    elif relationship.lower() in [x.lower() for x in sibling_in_laws_types]:
        relationship_result = 'sibling_in_law'
    elif relationship.lower() in [x.lower() for x in adult_child_types]:
        relationship_result = 'adult_child'
    elif relationship.lower() in [x.lower() for x in minor_child_types]:
        relationship_result = 'minor_child'
    else:
        relationship_result = relationship.lower()
    
    return relationship_result
