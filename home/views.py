from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.template import loader
from accounts.models import Profile

# Create your views here.
def index(request):
    #render_to_response returns the .html file
    user = request.user
    user_auth = user.is_authenticated()
    has_major = False
    major = ''

    if user_auth:
        try:
            current_user = Profile.objects.get(user=user)
            major = str(current_user.current_major)
            has_major = major != ''
        except ObjectDoesNotExist:
            pass

    context = {'user' : user, 'major': major, 'user_auth':user_auth, 'has_major': has_major}
    template = loader.get_template('home/index.html')
    return HttpResponse(template.render(context, request))