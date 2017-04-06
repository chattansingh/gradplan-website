from django import forms

class ClassRatingForm(forms.Form):

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
