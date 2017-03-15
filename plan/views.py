from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from testdata import road_map
from gradplan import getroadmap
from accounts.models import Profile
from forms import ChooseMajorForm, ChooseJobSalaries, ClassFilter, TimeFilter




def grad_road_map(request):
    user = request.user
    if user.is_authenticated():
        current_user = Profile.objects.get(user=request.user)
        url = current_user.graduation_plan
        if (url == None or url == ''):
            return redirect('/choosemajor')
    else:
        #user is anon, so redirect to the choose major
        return redirect('/choosemajor')
    #This needs to have the dynamic url that is passed based off the users gradplan
    # url = 'http://catalog.csun.edu/academics/comp/programs/bs-computer-science/'

    empty_filter = {'days': [], 'times': [], 'taken': []}
    road_map = getroadmap( url, empty_filter)

    #need to split up the road map to display it according to jesus styling
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



    context = {'road_map': road_map, 'year1':year1, 'year2':year2,'year3':year3, 'year4':year4}
    # template = 'plan/graduation_roadmap.html'
    template = 'plan/Plans.html'
    return render(request, template, context)

@csrf_exempt
def choose_a_major(request):
    user = request.user
    if request.method == 'POST':

        form = ChooseMajorForm(request.POST)

        if form.is_valid():

            template = 'plan/Plans.html'
            major_choice = str(form.cleaned_data['choose_major'])
            #save their choice for later if they are authenticated
            if user.is_authenticated():
                current_user = Profile.objects.get(user=user)
                current_user.graduation_plan = major_choice
                current_user.save()

            empty_filter = {'days': [], 'times': [], 'taken': []}
            road_map = getroadmap(major_choice, empty_filter)
            #maybe put this in a function?
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

            context = {'road_map': road_map, 'year1': year1, 'year2': year2, 'year3': year3, 'year4': year4}
            return render(request, template, context)
        else:
            template = 'accounts/save_error.html'
    else:
        template = 'plan/choose_major.html'
        form = ChooseMajorForm()
    return render(request, template, {'form': form,})

# TO view salaries
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
        major = 0
        template = 'plan/job_information.html'
        form = ChooseJobSalaries()

    return render(request, template, {'form': form, 'major': major})

@login_required
@csrf_exempt
def modify_gradplan(request):
    current_user = Profile.objects.get(user=request.user)

    if request.method == 'POST':

        class_form = ClassFilter(request.POST, instance=current_user)
        time_form = TimeFilter(request.POST)
        if class_form.is_valid() and time_form.is_valid():

            filtered_dictionary = {'days': [], 'times': [], 'taken': []}


            class_fliter = class_form.cleaned_data['class_list']
            filtered_dictionary['taken'] = [str(c) for c in class_fliter]

            monday = time_form.cleaned_data['monday']
            tuesday = time_form.cleaned_data['tuesday']
            wednesday = time_form.cleaned_data['wednesday']
            thursday = time_form.cleaned_data['thursday']
            friday = time_form.cleaned_data['friday']
            saturday = time_form.cleaned_data['saturday']

            if monday:
                filtered_dictionary['days'] = 'Mo'
                filtered_dictionary['times'].append([str(t) for t in monday])
            if tuesday:
                filtered_dictionary['days'] = 'Tu'
                filtered_dictionary['times'].append([str(t) for t in tuesday])
            if wednesday:
                filtered_dictionary['days'] = 'We'
                filtered_dictionary['times'].append([str(t) for t in wednesday])
            if thursday:
                filtered_dictionary['days'] = 'Th'
                filtered_dictionary['times'].append([str(t) for t in thursday])
            if friday:
                filtered_dictionary['days'] = 'Fr'
                filtered_dictionary['times'].append([str(t) for t in friday])
            if saturday:
                filtered_dictionary['days'] = 'Sa'
                filtered_dictionary['times'].append([str(t) for t in saturday])


            # empty_filter = {'days': [], 'times': [], 'taken': []}
            #Do the filtering here
            road_map = getroadmap(current_user.graduation_plan, filtered_dictionary)

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

            context = {'road_map': road_map, 'year1': year1, 'year2': year2, 'year3': year3, 'year4': year4}

            template = 'plan/Plans.html'
            return render(request, template, context)
        else:
            template = 'accounts/save_error.html'
            return render(request, template, {})
    else:
        # major = 0
        template = 'plan/modify_plan.html'
        class_form = ClassFilter(instance=current_user)
        time_form = TimeFilter()
        return render(request, template, {'class_form': class_form, 'time_form': time_form})