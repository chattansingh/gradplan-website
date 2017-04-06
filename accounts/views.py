from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render
from forms import InterestsForm, SuggestMajor
from models import Profile
from plan.suggest import suggest_plan
from plan.gradplan import getroadmap, format_gradplan

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
            result = 'Profile Updated!'
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
        result =''
        template = 'accounts/profile_form.html'
        form = InterestsForm(instance=current_user)
    return render(request, template, {'form': form, 'result': result})


def suggest_major(request):
    user_auth = request.user.is_authenticated()


    if request.method == 'POST':
        if user_auth:
            current_user = Profile.objects.get(user=request.user)

            form = SuggestMajor(request.POST, instance=current_user)

            if form.is_valid():
                result = 'Profile Updated!'
                #this needs to change to point to where we want to display their grad plan
                form.save()
                #this is a list of the choices
                #choices are 1, 2, 3, 4 1 = Science, 2 = Math..and so on.
                choices = form.cleaned_data['subject_interests']
                #problem was it was coming in unicode, have to change results to int
                choice = [int(item) for item in choices]
                # Based on users choices suggest to them a road map they can follow and save it as their current major
                url = suggest_plan(choice)
                current_user.graduation_plan = url
                current_user.save()
                return redirect('/roadmap')
            else:
                template = 'accounts/save_error.html'
                return render(request, template, {})
        else:
            template = 'plan/Plans.html'
            form = SuggestMajor(request.POST)
            if form.is_valid():
                choices = form.cleaned_data['subject_interests']
                # problem was it was coming in unicode, have to change results to int
                choice = [int(item) for item in choices]
                # Suggest a major based on choices but user is not logged in so cannot save
                url = suggest_plan(choice)
                empty_filter = {'days': [], 'times': [], 'taken': []}
                road_map = getroadmap(url, empty_filter)

                # need to split up the road map to display it according to jesus styling
                formatted_plan = format_gradplan(road_map)
                # user is not logged in -- ToDo: need to get the name of the major from the rodemap, will be easy when new system implemented
                major = ''
                has_major = False
                context = {'road_map': road_map,
                           'major': major, 'has_major': has_major}
                context.update(formatted_plan)
                return render(request, template, context)
            else:
                template = 'accounts/save_error.html'
                return render(request, template, {})
    else:
        result = ''
        template = 'accounts/suggest_major.html'
        choices = []
        form = SuggestMajor()
    return render(request, template, {'form': form, 'result': result, 'interests' : choices})
