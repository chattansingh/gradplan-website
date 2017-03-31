from django import forms
from professorrating.models import Professor

class ClassRatingForm(forms.Form):
    # class Meta:
    #     model = Professor
    #     exclude = ['first_name', 'last_name', 'number_of_ratings']

    RATING_SYSTEM = [
        (1, 'Poor'),
        (2, 'Eh...'),
        (3, 'Neutral'),
        (4, 'Recommend'),
        (5, 'Highly Recommend'),
        (6, 'Best Teacher I\'ve ever had'),
    ]

    number_rating = forms.ChoiceField(choices=RATING_SYSTEM, widget=forms.RadioSelect, required=True)
    rating = forms.CharField(widget=forms.Textarea)


# class AddProfessorForm(forms.ModelForm):
#
#
#
#     class Meta:
#         model = Professor
#         fields = ['first_name', 'last_name']