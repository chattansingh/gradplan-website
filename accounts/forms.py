from django import forms
from accounts.models import Profile
from plan.utilities import get_major_list


class InterestsForm(forms.ModelForm):
    #to store the user data
    SUBJECT_INTERESTS = (
        (1, 'Science'),
        (2, 'Math'),
        (3, 'History'),
        (4, 'Biology'),
        (5, 'Psychology'),
    )
    subject_interests = forms.MultipleChoiceField(choices=SUBJECT_INTERESTS
                                                  ,widget=forms.CheckboxSelectMultiple, required=False)

    # has_current_major_checkbox = forms.BooleanField(required=False)
    # current major

    MAJORS = get_major_list()
    current_major = forms.ChoiceField(choices=MAJORS, required=False)


    #finally figured it out at https://www.pydanny.com/core-concepts-django-modelforms.html

    class Meta:
        model = Profile
        exclude = [ 'user', 'subject_interests', 'graduation_plan']


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
        exclude = ['user', 'current_major', 'graduation_plan', 'major']


