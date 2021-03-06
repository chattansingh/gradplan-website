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

            classes_taken = self.classes_taken
            try:
                grad_plan = json.loads(self.grad_plan)
            except TypeError:
                grad_plan = self.grad_plan
            CLASS_LIST = []

            for sem in grad_plan:
                for c in sem['classes']:
                    if 'details' in c and not c['details'] == '' and len(c['details']['details']) > 1:
                        # ha to have the details key, not be empty and the details list must have something in it
                        tup_val = str(c['dept'] + ' ' + c['number'] + ' ' + c['details']['details'][0]['units'])
                    else:
                        tup_val = str(c['dept'] + ' ' + c['number'] + ' 3')
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
        ('0800h', '8:00am - 9:00am'),
        ('0900h', '9:00am - 10:00am'),
        ('1000h', '10:00am - 11:00am'),
        ('1100h', '11:00am - 12:00pm'),
        ('1200h', '12:00pm - 1:00pm'),
        ('1300h', '1:00pm - 2:00pm'),
        ('1400h', '2:00pm - 3:00pm'),
        ('1500h', '3:00pm - 4:00pm'),
        ('1600h', '4:00pm - 5:00pm'),
        ('1700h', '5:00pm - 6:00pm'),
        ('1800h', '6:00pm - 7:00pm'),
        ('1900h', '7:00pm - 8:00pm'),
        ('2000h', '8:00pm - 9:00pm'),
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
            counter = 0

            classes= []
            for sem in self.sem_class:
                counter+= 1
                class_name = str(sem['dept']) + " " +  str(sem['number'])
                if sem['details'] != '':
                    for details in sem['details']['details']:
                        tup_val = details['class_number']
                        for meetings in details['meetings']:
                            tup_val += ' ' + meetings['location'] + ' ' + meetings['days'] + ' ' + meetings['start_time']+ ' ' + meetings['end_time']
                        tup_display = tup_val
                        tup_val = class_name + ' ' + tup_val
                        tup = (tup_val, tup_display)
                        classes.append(tup)
                else:
                    tup_val = tup_display = class_name
                    tup = (tup_val, tup_display)
                    classes.append(tup)

                self.fields[class_name] = forms.ChoiceField(choices=classes, widget=forms.RadioSelect, required=False)
                classes = []





class SetUpSemesterClasses(forms.Form):

    NUMBER_CLASSES = [
        (1,'One Class'),
        (2,'Two Classes'),
        (3, 'Three Classes'),
        (4, 'Four Classes'),
        (5, 'Five Classes'),
        (6, 'Six Classes')

    ]

    choose_number_of_classes = forms.ChoiceField(choices=NUMBER_CLASSES, required=True)


class ChooseMultipleMajors(forms.Form):
    MAJORS = get_major_list()
    choose_multiple_majors = forms.MultipleChoiceField(choices=MAJORS, widget=forms.CheckboxSelectMultiple, required=True)