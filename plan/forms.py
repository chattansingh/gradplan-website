from django import forms
from accounts.models import Profile
from plan.gradplan import getroadmap


class ChooseMajorForm(forms.Form):

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
        ('Computer Science', 'Computer Science'),
        ('Electrical Engineering', 'Electrical Engineering'),
        ('Math (General)', 'Math (General)'),
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


class ChooseJobSalaries(forms.Form):

    MAJORS = (
        (1, 'Computer Science'),
        (2, 'Electrical Engineering'),
        (3, 'Math (General)'),
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


class ClassFilter(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     self.user = kwargs.pop('user', None)
    #     super(MyForm, self).__init__(*args, **kwargs)

    # fields = forms.fields_for_model(Profile)
    # url = Profile.graduation_plan.
    user_objects = Profile.objects.get(id=1)
    url = user_objects.graduation_plan
    empty_filter = {'days':[], 'times': [], 'taken': []}
    graduation_plan = getroadmap(url, empty_filter)
    CLASS_LIST = []

    for sem in graduation_plan:
        for c in sem['classes']:
            tup = (c['name'], c['name'])
            CLASS_LIST.append(tup)

    class_list = forms.MultipleChoiceField(choices=CLASS_LIST,
                                           widget=forms.CheckboxSelectMultiple,
                                           required=False)


    class Meta:
        model = Profile
        exclude = ['user', 'current_major', 'graduation_plan', 'major', 'subject_interests']

class TimeFilter(forms.Form):
    TIMES_DAYS = [
        ('8:00 AM', '8:00am - 9:00am'),
        ('9:00 AM', '9:00am - 10:00am'),
        ('10:00 AM', '10:00am - 11:00am'),
        ('11:00 AM', '11:00am - 12:00pm'),
        ('12:00 PM', '12:00pm - 1:00pm'),
        ('1:00 PM', '1:00pm - 2:00pm'),
        ('2:00 PM', '2:00pm - 3:00pm'),
        ('3:00 PM', '3:00pm - 4:00pm'),
        ('4:00 PM', '4:00pm - 5:00pm'),
        ('5:00 PM', '5:00pm - 6:00pm'),
        ('6:00 PM', '6:00pm - 7:00pm'),
        ('7:00 PM', '7:00pm - 8:00pm'),
        ('8:00 PM', '8:00pm - 9:00pm'),
    ]

    monday = forms.MultipleChoiceField(choices=TIMES_DAYS, widget=forms.CheckboxSelectMultiple, required=False)
    tuesday = forms.MultipleChoiceField(choices=TIMES_DAYS, widget=forms.CheckboxSelectMultiple, required=False)
    wednesday = forms.MultipleChoiceField(choices=TIMES_DAYS, widget=forms.CheckboxSelectMultiple, required=False)
    thursday = forms.MultipleChoiceField(choices=TIMES_DAYS, widget=forms.CheckboxSelectMultiple, required=False)
    friday = forms.MultipleChoiceField(choices=TIMES_DAYS, widget=forms.CheckboxSelectMultiple, required=False)
    saturday = forms.MultipleChoiceField(choices=TIMES_DAYS, widget=forms.CheckboxSelectMultiple, required=False)