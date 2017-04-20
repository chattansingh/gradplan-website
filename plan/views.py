from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from gradplan import getroadmap, get_major_url, format_gradplan, filter_gradplan
from accounts.models import Profile
from forms import ChooseMajorForm, ChooseJobSalaries, ClassFilter, TimeFilter
from plan import testdata



def grad_road_map(request):
    user = request.user
    # if user.is_authenticated():
    #     current_user = Profile.objects.get(user=request.user)
    #     url = current_user.graduation_plan
    #     major = current_user.current_major
    #     has_major = major != ''
    #
    #     if (url == None or url == ''):
    #         return redirect('/choosemajor')
    # else:
    #     #user is anon, so redirect to the choose major
    #     return redirect('/choosemajor')
    #This needs to have the dynamic url that is passed based off the users gradplan
    # url = 'http://catalog.csun.edu/academics/comp/programs/bs-computer-science/'
    #for testing purposes of new road map ############
    # empty_filter = {'days': [], 'times': [], 'taken': []}
    # road_map = getroadmap( url, empty_filter)
    # #need to split up the road map to display it according to jesus styling
    # formatted_gradplan = format_gradplan(road_map)
    # Separated the formatting code to gradplan
    # It returns a dictionary which you can just add to the current context
    #########################
    major = ''
    has_major = True
    import testdata
    road_map = testdata.road_map
    current_user = Profile.objects.get(user=user)
    progress = current_user.progress

    context = {'road_map': road_map, 'major':major, 'has_major':has_major, 'progress': progress}
    # context.update(formatted_gradplan)

    template = 'plan/Plans.html'
    return render(request, template, context)

@csrf_exempt
def choose_a_major(request):
    user = request.user
    major = ''
    if request.method == 'POST':

        form = ChooseMajorForm(request.POST)

        if form.is_valid():
            template = 'plan/Plans.html'
            major_choice = str(form.cleaned_data['choose_major'])
            #save their choice for later if they are authenticated
            if user.is_authenticated():
                current_user = Profile.objects.get(user=user)
                current_user.graduation_plan = get_major_url(major_choice)
                major = str(major_choice)
                current_user.save()
            else:
                major = ''

            empty_filter = {'days': [], 'times': [], 'taken': []}
            road_map = getroadmap(get_major_url(major_choice), empty_filter)
            # road_map = {}
            # need to split up the road map to display it according to jesus styling
            formatted_gradplan = format_gradplan(road_map)

            # Separated the formatting code to gradplan
            # It returns a dictionary which you can just add to the current context
            context = {'road_map': road_map, 'major': major}
            context.update(formatted_gradplan)
            return render(request, template, context)
        else:
            template = 'accounts/save_error.html'
    else:
        template = 'plan/choose_major.html'
        form = ChooseMajorForm()
    return render(request, template, {'form': form,})

# To view salaries
@csrf_exempt
def view_major_job_salaries(request):
    if request.method == 'POST':

        form = ChooseJobSalaries(request.POST)

        if form.is_valid():

            template = 'plan/job_information.html'

            major = int(form.cleaned_data['choose_major'])
            # save their choice for later if they are authenticated
        else:
            template = 'accounts/save_error.html'
            return render(request, template, {})
    else:
        
        template = 'plan/job_information.html'
        form = ChooseJobSalaries()

    return render(request, template, {'form': form, 'major': major})

@login_required
@csrf_exempt
def modify_gradplan(request):
    current_user = Profile.objects.get(user=request.user)
    # major = str(current_user.current_major)
    # grad_plan = current_user.graduation_plan
    grad_plan = testdata.road_map

    if request.method == 'POST':

        class_form = ClassFilter(request.POST, grad_plan=grad_plan)
        time_form = TimeFilter(request.POST)
        if class_form.is_valid() and time_form.is_valid():

            print class_form.cleaned_data['class_list']
            c = class_form.cleaned_data['class_list']
            # count the amount of units
            units_list = [units.split(' ')[1] for units in c]
            units_taken = 0
            for units in units_list:
                units_taken += int(units)

            print units_taken
            if current_user.classes_taken:
                classes_taken = class_form.cleaned_data['class_list']
                current_user.classes_taken += classes_taken
                current_user.progress = units_taken
                current_user.save()
                print current_user.progress
            else:
                current_user.classes_taken = class_form.cleaned_data['class_list']
                current_user.progress = units_taken
                current_user.save()
                print current_user.progress
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
        major = 0
        template = 'plan/modify_plan.html'

        if current_user.current_graduation_plan:
            class_form = ClassFilter(grad_plan=current_user.current_graduation_plan)
        else:
            class_form = ClassFilter(grad_plan=grad_plan)

        time_form = TimeFilter()
        return render(request, template, {'class_form': class_form, 'time_form': time_form, 'major': major})
