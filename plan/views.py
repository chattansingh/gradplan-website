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
    context = {'road_map': road_map}
    # template = 'plan/graduation_roadmap.html'
    template = 'plan/Plans.html'
    return render(request, template, context)