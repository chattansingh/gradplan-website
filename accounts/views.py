from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render
from forms import InterestsForm, SuggestMajor
from models import Profile


# Create your views here.
@login_required
# @transaction.atomic
def update_profile(request):
    current_user = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = InterestsForm(request.POST, instance=current_user)

        if form.is_valid():
            result = 'valid save'
            template = 'accounts/profile_form.html'
            form.save()
        else:
            result = 'not valid form'
            template = 'accounts/save_error.html'
    else:
        result ='not post'
        template = 'accounts/profile_form.html'
        # current_user = Profile.objects.get(request.user)
        form = InterestsForm(instance=current_user)
    return render(request, template, {'form': form, 'result': result})


def suggest_major(request):
    current_user = Profile.objects.get(user=request.user)

    if request.method == 'POST':

        form = SuggestMajor(request.POST, instance=current_user)

        if form.is_valid():
            result = 'valid save '
            #this needs to change to point to where we want to display their grad plan
            template = 'accounts/suggest_major.html'
            form.save()
            #this is a list of the choices
            #choices are 1, 2, 3, 4 1 = Science, 2 = Math..and so on.
            choices = form.cleaned_data['subject_interests']
            result = result + choices[0]
        else:

            template = 'accounts/save_error.html'
    else:
        result = ' not post'
        template = 'accounts/suggest_major.html'
        choices = []
        form = SuggestMajor(instance=current_user)
    return render(request, template, {'form': form, 'result': result, 'interests' : choices})
