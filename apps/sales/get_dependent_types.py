
child_types = ['Son', 'Daughter', 'Child']
parent_in_law_types = ['Parent In-Law', 'Mother in law', 'Father in law']
sibling_in_laws_types = ['Sibling In-Law', 'Brother in law', 'Brother-in-law', 'Sister in law', 'Son in law', 'Daughter in law']
grandparent_types = ['Grandparent', 'Grandfather', 'Grandmother']
grandchildren_types = ['Grandchild', 'Granddaughter', 'Grandson']
sibling_types = ['Sibling', 'Brother', 'Sister']
cousin_types = ['Cousin', 'cousin', 'COUSIN']
spouse_types = ['Spouse', 'Partner', 'Wife', 'Husband']
father_types = ['father', 'Step father', 'Step-Father']
mother_types = ['Mother', 'Step Mother', 'Step-Mother']

def get_relation_type(dependent_type: str):
    relation_type = ''
    if dependent_type.lower() in [x.lower() for x in child_types]:
        relation_type = 'child'
    elif dependent_type.lower() in [x.lower() for x in parent_in_law_types]:
        relation_type = 'parent_in_law'
    elif dependent_type.lower() in [x.lower() for x in sibling_in_laws_types]:
        relation_type = 'sibling_in_law'
    elif dependent_type.lower() in [x.lower() for x in grandparent_types]:
        relation_type = 'grandparent'
    elif dependent_type.lower() in [x.lower() for x in grandchildren_types]:
        relation_type = 'grandchild'
    elif dependent_type.lower() in [x.lower() for x in sibling_types]:
        relation_type = 'sibling'
    elif dependent_type.lower() in [x.lower() for x in cousin_types]:
        relation_type = 'cousin'
    elif dependent_type.lower() in [x.lower()  for x in spouse_types]:
        relation_type = 'spouse'
    elif dependent_type.lower() in [x.lower() for x in father_types]:
        relation_type = 'parent'
    elif dependent_type.lower() in [x.lower() for x in mother_types]:
        relation_type = 'parent'
    elif dependent_type == 'Adult Child':
        relation_type = 'adult_child'
    elif dependent_type == 'Minor Child':
        relation_type = 'minor_child'
    elif dependent_type == 'Senior Citizen Parent':
        relation_type = 'senior_citizen_parent'
    else:
        relation_type = dependent_type.lower()

    return relation_type