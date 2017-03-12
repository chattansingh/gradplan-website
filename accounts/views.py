from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render
from forms import InterestsForm


# Create your views here.
@login_required
# @transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        form = InterestsForm(request.POST, instance=request.user)

        if form.is_valid():
            template = 'accounts/profile_form.html'
            form.save()
        else:
            template = 'accounts/save_error.html'
    else:
        template = 'accounts/profile_form.html'
        form = InterestsForm(instance=request.user)
    return render(request, template, {'form': form,})


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
@login_required
# @transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        form = InterestsForm(request.POST, instance=request.user)

        if form.is_valid():
            template = 'accounts/profile_form.html'
            form.save()
        else:
            template = 'accounts/save_error.html'
    else:
        template = 'accounts/profile_form.html'
        form = InterestsForm(instance=request.user)
    return render(request, template, {'form': form,})


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
