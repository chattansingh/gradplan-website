from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.template import loader

# Create your views here.
def index(request):
    #render_to_response returns the .html file
    context = {}
    template = loader.get_template('home/index.html')
    return HttpResponse(template.render(context, request))
    #return HttpResponse("Hello world.  You're at the home index")