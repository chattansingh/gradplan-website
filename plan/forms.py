from django import forms
from plan.utilities import get_major_list
import json

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
            grad_plan = json.loads(self.grad_plan)
            classes_taken = self.classes_taken
            CLASS_LIST = []

            for sem in grad_plan:
                for c in sem['classes']:
                    if 'details' in c and not c['details'] == '' and len(c['details']) > 1:
                        # ha to have the details key, not be empty and the details list must have something in it
                        tup_val = str(c['dept'] + c['number'] + ' ' + c['details'][0]['units'])
                    else:
                        tup_val = str(c['dept'] + c['number'] + ' 3')
                    tup_display = str(c['dept'] + c['number'])
                    tup = (tup_val, tup_display)
                    # if the current class has not already been filtered add it to the form
                    if classes_taken:
                        if not tup_val in classes_taken:
                            CLASS_LIST.append(tup)
                    else:
                        # if the classes taken is null, just append everything
                        # this is a new user or someone who has not taken any classes
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

# going to create individual forms for each class
class SemesterClass(forms.Form):

    def __init__(self, *args, **kwargs):
        self.sem_class = kwargs.pop('sem_class', None)
        super(SemesterClass, self).__init__(*args, **kwargs)
        if self.sem_class:

            CLASSES= []
            for sem in self.sem_class:
                class_name = str(sem['dept']) + str(sem['number'])
                for details in sem['details']:
                    tup_val = class_name + ' ' + details['class_number']
                    for meetings in details['meetings']:
                        tup_val += ' ' + meetings['location'] + ' ' + meetings['days'] + ' ' + meetings['start_time']+ ' ' + meetings['end_time']
                    tup_display = tup_val
                    tup = (tup_val, tup_display)
                    CLASSES.append(tup)
            self.fields['sem_classess'] = forms.ChoiceField(choices=CLASSES, widget=forms.CheckboxSelectMultiple, required=False)

    sem_classes = forms.ChoiceField()



