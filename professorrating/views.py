from django.shortcuts import render
from models import Professor, ClassRating
from forms import ClassRatingForm


# Create your views here.
def rate_professor(request):
    first_name = 'Vahab'
    last_name = 'Pournaghshband'
    class_name = 'COMP110'

    # if request.method == 'POST':
    try:
        professor = Professor.objects.get(first_name=first_name, last_name=last_name)

    except Professor.DoesNotExist:
        professor = Professor(first_name=first_name, last_name=last_name)
        professor.save()

    try:
        class_ratings = ClassRating.objects.filter(professor=professor, class_name=class_name)
        has_ratings = True
    except ClassRating.DoesNotExist:
        # Prof has no entries need set a different market so that the template will create it
        has_ratings = False

    form = ClassRatingForm()
    template = 'professorrating/addrating.html'
    context = {
        'form': form,
        'class_ratings': class_ratings,
        'professor': professor,
        'has_ratings': has_ratings,
        'class_name': class_name,
    }
    # else:
    #     template = 'professorrating/youshouldntbehere.html'
    #     context = {}

    return render(request, template, context)
