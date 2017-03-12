from django.shortcuts import render

# Create your views here.
from testdata import road_map
from gradplan import getroadmap

def grad_road_map(request):

    #This needs to have the dynamic url that is passed based off the users gradplan
    url = 'http://catalog.csun.edu/academics/comp/programs/bs-computer-science/'
    road_map = getroadmap( url, {})
    context = {'road_map': road_map}
    template = 'plan/graduation_roadmap.html'
    return render(request, template, context)