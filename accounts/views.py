from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render
from forms import InterestsForm, SuggestMajor
from models import Profile
from plan.suggest import suggest_plan
from plan.gradplan import getroadmap

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
        # current_user = Profile.objects.get(request.user)
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
                return render(request, template, {})
        else:
            template = 'plan/Plans.html'
            form = SuggestMajor(request.POST)
            if form.is_valid():
                choices = form.cleaned_data['subject_interests']
                choice = []
                # problem was it was coming in unicode, have to change results to int
                for item in choices:
                    choice.append(int(item))
                url = suggest_plan(choice)
                empty_filter = {'days': [], 'times': [], 'taken': []}
                road_map = getroadmap(url, empty_filter)

                # need to split up the road map to display it according to jesus styling
                counter = 1
                year1 = []
                year2 = []
                year3 = []
                year4 = []

                for semester in road_map:
                    if counter == 1 or counter == 2:
                        year1.append(semester)
                    elif counter == 3 or counter == 4:
                        year2.append(semester)
                    elif counter == 5 or counter == 6:
                        year3.append(semester)
                    elif counter == 7 or counter == 8:
                        year4.append(semester)
                    counter = counter + 1
                major = ''
                has_major = False
                context = {'road_map': road_map, 'year1': year1, 'year2': year2, 'year3': year3, 'year4': year4,
                           'major': major, 'has_major': has_major}
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
