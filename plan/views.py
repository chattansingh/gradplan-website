from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from gradplan import getroadmap, get_major_url, format_gradplan, filter_gradplan
from accounts.models import Profile
from forms import ChooseMajorForm, ChooseJobSalaries, ClassFilter, TimeFilter
from plan.models import MajorRoadMaps
from plan.utilities import get_semester
import json



def grad_road_map(request):
    user = request.user
    if user.is_authenticated():
        current_user = get_object_or_404(Profile, user=request.user)
        #get the current graduation plan that the user has selected
        road_map = current_user.current_graduation_plan
        major = current_user.current_major
        progress = current_user.progress
        has_major = major != ''

        if grad_road_map == None:
            return redirect('/choosemajor')

    else:
        #user is anon, so redirect to the choose major
        return redirect('/choosemajor')

    # ToDo: This may not be needed, could be redundant
    if not has_major:
        major = ''
    print 'processing web page....'
    if road_map:
        dic = get_semester(road_map)
    else:
        return redirect('/choosemajor')

    # print dic['remaining_sem']

    context = {'major':major, 'has_major':has_major, 'progress': progress}
    context.update(get_semester(road_map))
    template = 'plan/Plans.html'
    return render(request, template, context)

# @csrf_exempt
def choose_a_major(request):
    user = request.user

    if request.method == 'POST':

        form = ChooseMajorForm(request.POST)

        if form.is_valid():
            template = 'plan/Plans.html'
            major_choice = form.cleaned_data['choose_major'].encode('utf-8')
            maj_obj = get_object_or_404(MajorRoadMaps, major=major_choice)
            road_map = maj_obj.road_map
            progress = 0
            #save their choice for later if they are authenticated
            if user.is_authenticated():
                current_user = get_object_or_404(Profile, user=user)

                current_user.base_graduation_plan = road_map
                current_user.current_graduation_plan = road_map
                progress = current_user.progress
                major = major_choice
                current_user.save()
            else:
                # annon user
                major = maj_obj.major
                road_map = maj_obj.road_map

            # empty_filter = {'days': [], 'times': [], 'taken': []}
            # road_map = getroadmap(get_major_url(major_choice), empty_filter)
            # road_map = {}
            # need to split up the road map to display it according to jesus styling
            # formatted_gradplan = format_gradplan(road_map)
            has_major = True

            # Separated the formatting code to gradplan
            # It returns a dictionary which you can just add to the current context
            context = {'major': major, 'has_major':has_major, 'progress': progress}
            # update it with split up semesters to more easily display it
            # keys are 'detail_sem' and 'remaining_sem'
            print 'processing web page....'
            context.update(get_semester(road_map))
            return render(request, template, context)
        else:
            template = 'accounts/save_error.html'
    else:
        template = 'plan/choose_major.html'
        form = ChooseMajorForm()
    return render(request, template, {'form': form,})

# To view salaries
# ToDo: this needs to be completely overhauled to not be hard coded
# @csrf_exempt
def view_major_job_salaries(request):
    major = ''
    if request.method == 'POST':

        form = ChooseJobSalaries(request.POST)

        if form.is_valid():

            template = 'plan/job_information.html'

            major = form.cleaned_data['choose_major'].encode('utf-8')
            # save their choice for later if they are authenticated
        else:
            template = 'accounts/save_error.html'
            return render(request, template, {})
    else:
        
        template = 'plan/job_information.html'
        form = ChooseJobSalaries()

    return render(request, template, {'form': form, 'major': major})

@login_required
# @csrf_exempt
def modify_gradplan(request):
    current_user = get_object_or_404(Profile, user=request.user)

    major = current_user.current_major
    grad_plan = current_user.current_graduation_plan

    if request.method == 'POST':

        class_form = ClassFilter(request.POST, grad_plan=grad_plan)
        time_form = TimeFilter(request.POST)
        if class_form.is_valid() and time_form.is_valid():
            c = class_form.cleaned_data['class_list']
            # count the amount of units
            units_list = [units.split(' ')[-1] for units in c]
            units_taken = 0
            for units in units_list:
                units_taken += int(units)

            if current_user.classes_taken:
                # append the classes that they have already taken
                classes_taken = class_form.cleaned_data['class_list']
                current_user.classes_taken += classes_taken
                current_user.progress = units_taken
                current_user.save()
            else:
                # user has not taken any other classes
                current_user.classes_taken = class_form.cleaned_data['class_list']
                current_user.progress = units_taken
                current_user.save()
            #Do the filtering here
            # filtered_dictionary = filter_gradplan(class_form, time_form)
            #Get a revised roadmap
            # road_map = getroadmap(current_user.graduation_plan, filtered_dictionary)
            # Formate the road map to display it according to jesus styling
            # formatted_gradplan = format_gradplan(road_map)
            # Separated the formatting code to gradplan
            # It returns a dictionary which you can just add to the current context

            # context = {'road_map': road_map, 'major': major}
            # context.update(formatted_gradplan)


            context = {}
            template = 'plan/Plans.html'
            return render(request, template, context)
        else:
            template = 'accounts/save_error.html'
            return render(request, template, {})
    else:
        # not a post
        template = 'plan/modify_plan.html'

        class_form = ClassFilter(grad_plan=current_user.current_graduation_plan, classes_taken=current_user.classes_taken)


        time_form = TimeFilter()
        return render(request, template, {'class_form': class_form, 'time_form': time_form, 'major': major})
