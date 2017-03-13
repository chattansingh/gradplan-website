from django.shortcuts import render

# Create your views here.
from testdata import road_map
from gradplan import getroadmap
from accounts.models import Profile

def grad_road_map(request):

    current_user = Profile.objects.get(user=request.user)
    url = current_user.graduation_plan
    #This needs to have the dynamic url that is passed based off the users gradplan
    # url = 'http://catalog.csun.edu/academics/comp/programs/bs-computer-science/'
    road_map = getroadmap( url, {})

    #need to split up the roadmap
    counter = 1
    year1 =[]
    year2 =[]
    year3 =[]
    year4 =[]

    for semester in road_map:
        if counter == 1 or counter ==2:
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