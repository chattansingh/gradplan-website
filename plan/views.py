from django.shortcuts import render

# Create your views here.
from testdata import road_map
from gradplan import getroadmap

def grad_road_map(request):

    road_map = getroadmap('http://catalog.csun.edu/academics/comp/programs/bs-computer-science/', {})
    context = {'road_map': road_map}
    template = 'plan/graduation_roadmap.html'
    return render(request, template, context)