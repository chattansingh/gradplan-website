from django.shortcuts import render

# Create your views here.
from testdata import road_map

def grad_road_map(request):


    context = {'road_map': road_map}
    template = 'plan/graduation_roadmap.html'
    return render(request, template, context)