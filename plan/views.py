from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from gradplan import getroadmap, get_major_url, format_gradplan, filter_gradplan
from accounts.models import Profile
from forms import ChooseMajorForm, ChooseJobSalaries, ClassFilter, TimeFilter, SemesterClass, SetUpSemesterClasses, ChooseMultipleMajors
from plan.models import MajorRoadMaps
from plan.utilities import get_semester, get_common_classes
import json


def grad_road_map(request):
    user = request.user
    if user.is_authenticated():
        current_user = get_object_or_404(Profile, user=request.user)
        # get the current graduation plan that the user has selected
        road_map = current_user.current_graduation_plan
        major = current_user.current_major
        progress = current_user.progress
        has_major = major != ''

        if grad_road_map == None:
            return redirect('/choosemajor')

    else:
        # user is anon, so redirect to the choose major
        return redirect('/choosemajor')

    # ToDo: This may not be needed, could be redundant
    if not has_major:
        major = ''
    print 'processing web page....'
    if not road_map:
        return redirect('/choosemajor')

    # print dic['remaining_sem']

    context = {'major': major, 'has_major': has_major, 'progress': progress}
    dictionary = get_semester(road_map)
    context.update(dictionary)
    template = 'plan/Plans.html'
    return render(request, template, context)



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
            # save their choice for later if they are authenticated
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
            context = {'major': major, 'has_major': has_major, 'progress': progress}
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
    return render(request, template, {'form': form, })


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
def modify_gradplan(request):
    current_user = get_object_or_404(Profile, user=request.user)

    major = current_user.current_major
    grad_plan = current_user.current_graduation_plan

    if request.method == 'POST':

        class_form = ClassFilter(request.POST, grad_plan=grad_plan)
        if class_form.is_valid():
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
                current_user.progress += units_taken
                current_user.save()
            # Do the filtering here
            # filtered_dictionary = filter_gradplan(class_form, time_form)
            # Get a revised roadmap
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

        class_form = ClassFilter(grad_plan=current_user.current_graduation_plan,
                                 classes_taken=current_user.classes_taken)

        time_form = TimeFilter()
        return render(request, template, {'class_form': class_form, 'major': major})


@login_required
def current_semester(request):
    current_user = get_object_or_404(Profile, user=request.user)
    current_semester = current_user.current_semester

    if current_semester:

        context = {'classes': current_semester}
        template = 'plan/current_semester.html'
    else:
        return redirect('/plan/choosesemester')

    return render(request, template, context)


@login_required
def choose_semester(request):
    current_user = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        if request.POST['classes'] == 'Get Classes':
            # Do the filtering of classes
            #     This is disabling the forms for the page
            filter_time = False
            choose_classes = True
            template = 'plan/choose_semester.html'
            current_graduation_plan = current_user.current_graduation_plan
            semester = get_semester(current_graduation_plan)['detail_sem']
            select_classes_form = SemesterClass(sem_class=semester)
            return render(request, template,
                          {'select_classes_form': select_classes_form,
                           'filter_time': filter_time, 'select_classes': choose_classes})
        else:
            classes_chosen = SemesterClass(request.POST)

            if classes_chosen.is_valid():
                classes = []
                for key in classes_chosen.data:
                    if key != 'csrfmiddlewaretoken':
                        classes.append(classes_chosen.data[key])

                current_user.current_semester = classes
                current_user.save()

        return render(request, 'plan/current_semester.html', {'classes': classes})
    else:
        filter_time = True
        choose_classes = False
        time_filter_form = TimeFilter()

        # create a form for each class
        # forms = {}
        # count = 0
        # for sem in semester:
        #     count += 1
        #     key = 'class_form_' + count
        #     forms.update({key : SemesterClass(sem_class=sem)})

        template = 'plan/choose_semester.html'

        return render(request, template, {'time_filter_form': time_filter_form, 'filter_time': filter_time, 'choose_classes': choose_classes})


@login_required
def common_classes(request):
    current_user = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = ChooseMultipleMajors(request.POST)
        if form.is_valid():
            majors_chosen = form.cleaned_data['choose_multiple_majors']
            road_maps = [MajorRoadMaps.objects.get(major=major).road_map for major in majors_chosen]
            context = {'detail_sem': get_common_classes(road_maps)}
            return render(request, 'plan/Plans.html', context)
        else:
            return redirect('roadmap/commonclasses/')
    else:
        form = ChooseMultipleMajors()
        return render(request, 'plan/choose_common.html', {'form': form})