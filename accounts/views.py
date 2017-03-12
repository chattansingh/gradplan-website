from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render
from forms import InterestsForm
from models import Profile


# Create your views here.
@login_required
# @transaction.atomic
def update_profile(request):
    current_user = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = InterestsForm(request.POST, instance=current_user)

        if form.is_valid():
            result = 'valid save'
            template = 'accounts/profile_form.html'
            form.save()
        else:
            result = 'not valid form'
            template = 'accounts/save_error.html'
    else:
        result ='not post'
        template = 'accounts/profile_form.html'
        # current_user = Profile.objects.get(request.user)
        form = InterestsForm(instance=current_user)
    return render(request, template, {'form': form, 'result': result})


def suggest_major(request):
    if request.method == 'POST':
        form = InterestsForm(request.POST, instance=request.user)

        if form.is_valid():
            template = 'accounts/suggest_major.html'
            form.save()
        else:
            template = 'accounts/suggest_major.html'
    else:
        template = 'accounts/suggest_major.html'
        form = InterestsForm(instance=request.user)
    return render(request, template, {'form': form,})
