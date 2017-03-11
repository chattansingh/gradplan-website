
# from django import forms
#
# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Submit, Layout, Field
# from crispy_forms.bootstrap import (
#     PrependedText, PrependedAppendedText, FormActions)
#
# class SimpleForm(forms.Form):
#     username = forms.CharField(label="Username", required=True)
#     password = forms.CharField(
#         label="Password", required=True, widget=forms.PasswordInput)
#     remember = forms.BooleanField(label="Remember Me?")
#
#     helper = FormHelper()
#     helper.form_method = 'POST'
#     helper.add_input(Submit('login', 'login', css_class='btn-primary'))
#
# class CartForm(forms.Form):
#     item = forms.CharField()
#     quantity = forms.IntegerField(label="Qty")
#     price = forms.DecimalField()
#
#     helper = FormHelper()
#     helper.form_method = 'POST'
#     helper.layout = Layout(
#         'item',
#         PrependedText('quantity', '#'),
#         PrependedAppendedText('price', '$', '.00'),
#         FormActions(Submit('login', 'login', css_class='btn-primary'))
#     )
#
#
# class CreditCardForm(forms.Form):
#     fullname = forms.CharField(label="Full Name", required=True)
#     card_number = forms.CharField(label="Card", required=True, max_length=16)
#     expire = forms.DateField(label="Expire Date", input_formats=['%m/%y'])
#     ccv = forms.IntegerField(label="ccv")
#     notes = forms.CharField(label="Order Notes", widget=forms.Textarea())
#
#     helper = FormHelper()
#     helper.form_method = 'POST'
#     helper.form_class = 'form-horizontal'
#     helper.label_class = 'col-sm-2'
#     helper.field_class = 'col-sm-4'
#     helper.layout = Layout(
#         Field('fullname', css_class='input-sm'),
#         Field('card_number', css_class='input-sm'),
#         Field('expire', css_class='input-sm'),
#         Field('ccv', css_class='input-sm'),
#         Field('notes', rows=3),
#         FormActions(Submit('purchase', 'purchase', css_class='btn-primary'))
#     )

from django import forms
from accounts.models import Profile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from crispy_forms.bootstrap import (PrependedText, PrependedAppendedText, FormActions)


class InterestsForm(forms.ModelForm):
    #to store the user data
    # SUBJECT_INTERESTS = (
    #     (1, 'Science'),
    #     (2, 'Math'),
    #     (3, 'History'),
    #     (4, 'Biology'),
    #     (5, 'Psychology'),
    # )
    # subject_interests = forms.MultipleChoiceField(choices=SUBJECT_INTERESTS
    #                                               ,widget=forms.CheckboxSelectMultiple, required=False)

    has_current_major_checkbox = forms.BooleanField(required=False)
    # current major
    MAJORS = (
        ('Computer Science', 'Computer Science'),
        ('Electrical Engineering', 'Electrical Engineering'),
        ('History', 'History'),
        ('Art', 'Art'),
    )
    current_major = forms.ChoiceField(choices=MAJORS, required=False)
    graduation_plan = forms.CharField(required=False)
    # blank = True means the feild is nto required

    #finally figured it out at https://www.pydanny.com/core-concepts-django-modelforms.html

    class Meta:
        model = Profile
        exclude = [ 'user', 'subject_interests']


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


    #multi Checkbox field
    #
    # #Crispy Form helper object
    # #used to define the forms attributes
    # form_helper = FormHelper()
    # #Save button
    # #form_helper.form_method = 'POST'
    # form_helper.layout = Layout(
    #     has_current_major_checkbox,
    #     PrependedText('current_major_dropdown', 'Choose Major'),
    #     subject_interests,
    # )
    # form_helper.add_input(Submit('submit','submit'))

