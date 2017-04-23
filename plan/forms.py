from django import forms
from plan.utilities import get_major_list


class ChooseMajorForm(forms.Form):

    MAJORS = get_major_list()
    choose_major = forms.ChoiceField(choices=MAJORS, required=False)


class ChooseJobSalaries(forms.Form):

    MAJORS = get_major_list()
    choose_major = forms.ChoiceField(choices=MAJORS, required=False)


class ClassFilter(forms.Form):
    # Display all of the classes in check box
    # Fixed this to take the keyword argument of the current user rather than doing a lookup
    # it was breaking the database
    def __init__(self, *args, **kwargs):
        self.grad_plan = kwargs.pop('grad_plan', None)
        self.classes_taken = kwargs.pop('classes_taken', None)
        super(ClassFilter, self).__init__(*args, **kwargs)
        if self.grad_plan:
            grad_plan = self.grad_plan
            classes_taken = self.classes_taken
            CLASS_LIST = []

            for sem in grad_plan:
                for c in sem['classes']:
                    tup_val = str(c['dept'] + c['details']['number'] + ' ' + c['details']['units'])
                    tup_display = str(c['dept'] + c['details']['number'])
                    tup = (tup_val, tup_display)
                    # if the current class has not already been filtered add it to the form
                    if not tup_val in classes_taken:
                        CLASS_LIST.append(tup)
            self.fields['class_list'] = \
                forms.MultipleChoiceField(choices=CLASS_LIST, widget=forms.CheckboxSelectMultiple, required=False)

    class_list = forms.MultipleChoiceField()


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