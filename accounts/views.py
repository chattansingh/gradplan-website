from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render
from forms import InterestsForm, SuggestMajor
from models import Profile
from plan.suggest import suggest_plan

#parse choice into url
#just thought of it, I could probably jhust change this on the forms
def get_major_url(major):
    if major == 'Electrical Engineering':
        return 'http://catalog.csun.edu/academics/ece/programs/bs-electrical-engineering/'
    if major == 'Computer Science':
        return 'http://catalog.csun.edu/academics/comp/programs/bs-computer-science/'
    if major == 'Math':
        return 'http://catalog.csun.edu/academics/math/programs/ba-mathematics-i/general/'

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
            major_choice = str(form.cleaned_data['current_major'])
            major_choice = get_major_url(major_choice)

            current_user.graduation_plan = major_choice
            current_user.save()
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
            choice = []
            #problem was it was coming in unicode, have to change results to int
            for item in choices:
                choice.append(int(item))
            url = suggest_plan(choice)
            # url = 'http://catalog.csun.edu/academics/comp/programs/bs-computer-science/' #erase me
            current_user.graduation_plan = url
            current_user.save()

            # result = result + choices[0]

            return redirect('/roadmap')
        else:

            template = 'accounts/save_error.html'
    else:
        result = ' not post'
        template = 'accounts/suggest_major.html'
        choices = []
        form = SuggestMajor(instance=current_user)
    return render(request, template, {'form': form, 'result': result, 'interests' : choices})
