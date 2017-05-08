from django import forms
from accounts.models import Profile
from plan.utilities import get_major_list


class InterestsForm(forms.ModelForm):
    #to store the user data
    # has_current_major_checkbox = forms.BooleanField(required=False)
    # current major

    MAJORS = get_major_list()
    current_major = forms.ChoiceField(choices=MAJORS, required=False)


    #finally figured it out at https://www.pydanny.com/core-concepts-django-modelforms.html

    class Meta:
        model = Profile
        fields = ['current_major']

class SuggestMajor(forms.ModelForm):

    #to store the user data
    SUBJECT_INTERESTS = (
        (1, 'Science'),
        (2, 'Math'),
        (3, 'History'),
        (4, 'Biology'),
        (5, 'Psychology'),
    )
    subject_interests = forms.MultipleChoiceField(choices=SUBJECT_INTERESTS,
                                                  widget=forms.CheckboxSelectMultiple,
                                                  required=False)

    class Meta:
        model = Profile
        fields = ['subject_interests']


class EditClasses(forms.Form):
    def __init__(self, *args, **kwargs):
        self.classes_taken = kwargs.pop('classes_taken', None)
        super(EditClasses, self).__init__(*args, **kwargs)
        if self.classes_taken:
            CLASSES_TAKEN = []
            for item in self.classes_taken:
                CLASSES_TAKEN.append((item,item))
            self.fields['classes'] = forms.MultipleChoiceField(choices=CLASSES_TAKEN, widget=forms.CheckboxSelectMultiple, required=False)


    classes = forms.MultipleChoiceField()

