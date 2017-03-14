from django import forms


class ChooseMajorForm(forms.Form):
    comp_sci = 'http://catalog.csun.edu/academics/comp/programs/bs-computer-science/'
    math = 'http://catalog.csun.edu/academics/math/programs/ba-mathematics-i/general/'
    electrical = 'http://catalog.csun.edu/academics/ece/programs/bs-electrical-engineering/'
    # art = 'http://catalog.csun.edu/academics/art/programs/ba-art/'
    # accounting = 'http://catalog.csun.edu/academics/acctis/programs/bs-accountancy/'
    # african_studies ='http://catalog.csun.edu/academics/afric/programs/minor-african-studies/'
    # anthropology = 'http://catalog.csun.edu/academics/anth/programs/ba-anthropology/'
    # biology = 'http://catalog.csun.edu/academics/biol/programs/ba-biology/'
    # business_law = 'http://catalog.csun.edu/academics/blaw/programs/bs-business-administration-i/business-law/'
    # california_studies = 'http://catalog.csun.edu/academics/calif/programs/minor-california-studies/'
    # marketing ='http://catalog.csun.edu/academics/mkt/programs/bs-marketing/'
    # nursing = 'http://catalog.csun.edu/academics/nurs/programs/bsn-nursing-ii/accelerated/'

    MAJORS = (
        (comp_sci, 'Computer Science'),
        (electrical, 'Electrical Engineering'),
        (math, 'Math (General)'),
        # (art, 'Art'),
        # (accounting, 'Accounting'),
        # (african_studies, 'African Studies'),
        # (anthropology, 'Anthropology'),
        # (biology, 'Biology'),
        # (business_law, 'Business Law'),
        # (california_studies, 'California Studies'),
        # (marketing, 'Marketing'),
        # (nursing, 'Nursing'),
    )
    choose_major = forms.ChoiceField(choices=MAJORS, required=False)