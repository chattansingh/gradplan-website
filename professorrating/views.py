from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from models import Professor, ClassRating
from forms import ClassRatingForm


# Create your views here.
# @login_required
def rate_professor(request, last_name, first_name, class_name):
    first_name = str(first_name.title())
    last_name = str(last_name.title())
    class_name = str(class_name)

    # ToDo: NOTE THIS MAY NEED TO BE RESTRICTED SO USER CAN ONLY RATE ONE TIME, OR IT REPLACES SO USER CANT SPAM


    if request.method == 'POST':
        # Get form data
        form = ClassRatingForm(request.POST)

        if form.is_valid():
            # form contains number_rating (int), rating (char)
            rating_number = int(form.cleaned_data['number_rating'])
            rating = str(form.cleaned_data['rating'])
            # attempt to query the professor in the database
            try:
                # ToDo: there is an error here...something going wrong with the average rating
                professor = Professor.objects.get(first_name=first_name, last_name=last_name)
                # Add to his average rating
                total_rating = professor.total_rating

                number_of_ratings = professor.number_of_ratings

                number_of_ratings += 1 #increment the number of ratings
                total_rating = total_rating + rating_number #add given rating to professor total
                average_rating = total_rating / number_of_ratings
                professor.average_rating = average_rating
                professor.total_rating = total_rating
                professor.number_of_ratings = number_of_ratings
                professor.save()

            except Professor.DoesNotExist:
                template = 'accounts/save_error.html'
                error = 'Professor ' + str(last_name) + ', ' + str(first_name) + ' doesnt exist.'
                context = {'error': error}
                return render(request, template, context)
            # Save the new rating to the professor
            try:
                # ToDo: Fix the class id issue.  Need to have that pass through like the class name
                new_rating = ClassRating(professor=professor, class_name=class_name, rating=rating, number_rating=rating_number, class_id=10010)
                new_rating.save()

            except ClassRating.AttributeError:
                template = 'accounts/save_error.html'
                error = 'Error saving class rating'
                context = {'error': error}
                return render(request, template, context)


        else:
            template = 'accounts/save_error.html'

    # ToDo: There could be an issue where you can create your own professors through the url
    try:
        professor = Professor.objects.get(first_name=first_name, last_name=last_name)

    except Professor.DoesNotExist:
        template = 'accounts/save_error.html'
        error = 'Professor ' + str(last_name) + ', ' + str(first_name) + ' doesnt exist.'
        context = {'error': error}
        return render(request, template, context)

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
        'class_name': str(class_name),
    }
    # else:
    #     template = 'professorrating/youshouldntbehere.html'
    #     context = {}

    return render(request, template, context)
