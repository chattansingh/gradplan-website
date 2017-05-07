from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render
from forms import InterestsForm, SuggestMajor, EditClasses
from models import Profile
from plan.suggest import suggest_plan
from plan.gradplan import getroadmap, format_gradplan
from plan.models import MajorRoadMaps
import json

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
            template = 'accounts/profile_form.html'
            major_choice = form.cleaned_data['current_major'].encode('utf-8')
            maj_obj = get_object_or_404(MajorRoadMaps, major=major_choice)
            road_map = maj_obj.road_map
            current_user.current_major = maj_obj.major
            current_user.base_graduation_plan = road_map
            current_user.current_graduation_plan = road_map
            current_user.save()
            form.save()
            progress = current_user.progress
            classes_taken = current_user.classes_taken
            return render(request, template, {'form': form, 'progress': progress, 'classes_taken': classes_taken})
        else:
            template = 'accounts/save_error.html'
            return render(request, template, { })
    else:
        template = 'accounts/profile_form.html'
        form = InterestsForm(instance=current_user)
        progress = current_user.progress
        classes_taken = current_user.classes_taken
        return render(request, template, {'form': form, 'progress': progress, 'classes_taken': classes_taken})



@login_required
def edit_classes(request):
    current_user = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        classes_taken = current_user.classes_taken
        remove_form = EditClasses(request.POST, classes_taken=classes_taken)


        # ERROR HERE SOMETHING TO DO WITH NOT RESPONSE, AND TO DO WITH THE FORM
        if remove_form.is_valid():
            classes_taken = current_user.classes_taken
            classes_to_remove = remove_form.cleaned_data['classes']
            units_to_remove = 0
            for item in classes_to_remove:
                classes_taken.remove(item.encode('utf-8'))
                units_to_remove += int(item.split(' ')[-1])

            current_user.classes_taken = classes_taken
            current_user.progress -= units_to_remove
            current_user.save()

            template = 'accounts/profile_form.html'
            form = InterestsForm(instance=current_user)
            progress = current_user.progress
            classes_taken = current_user.classes_taken
            # return render(request, template,
            #               {'form': form, 'progress': progress, 'classes_taken': classes_taken})
            return redirect('/profile/')
        else:
            return redirect('/profile/')

    else:
        classes_taken = current_user.classes_taken
        form = EditClasses(classes_taken=classes_taken)
        template = 'accounts/edit_classes_taken.html'
        return render(request, template, {'form': form})


def suggest_major(request):


    if request.method == 'POST':
        user_auth = request.user.is_authenticated()
        if user_auth:
            current_user = get_object_or_404(Profile, user=request.user)

            form = SuggestMajor(request.POST, instance=current_user)

            if form.is_valid():
                result = 'Profile Updated!'
                #this needs to change to point to where we want to display their grad plan
                #this is a list of the choices
                #choices are 1, 2, 3, 4 1 = Science, 2 = Math..and so on.
                choices = form.cleaned_data['subject_interests']
                #problem was it was coming in unicode, have to change results to int
                choice = [int(item) for item in choices]
                # Based on users choices suggest to them a road map they can follow and save it as their current major
                major = suggest_plan(choice)
                maj_obj = get_object_or_404(MajorRoadMaps, major=major)
                current_user.current_major = maj_obj.major
                current_user.graduation_plan = maj_obj.road_map
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
                major = suggest_plan(choice)
                maj_obj = get_object_or_404(MajorRoadMaps, major=major)
                road_map = maj_obj.road_map

                # need to split up the road map to display it according to jesus styling
                # user is not logged in -- ToDo: need to get the name of the major from the roadmap, will be easy when new system implemented
                major = maj_obj.major
                has_major = True
                context = {'road_map': road_map,
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
