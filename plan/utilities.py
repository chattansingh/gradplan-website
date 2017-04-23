#various utilites
from plan.models import MajorRoadMaps


def get_prof_email_name(email):
    #takes the professors email and returns the first and last name on the email
    #hopefully only returns only first or last if in form first@csun.edu or last@csun.edu
    try:
        return [p.capitalize() for p in email.split('@')[0].split('.')]
    except IndexError:
        return []

#this is to return a list of all the majors by their name
#Will help with creation of drop downs in forms
def get_major_list():

    majors = []
    query_list = MajorRoadMaps.objects.filter()
    for maj in query_list:
        majors.append((maj.major.encode('utf-8'),maj.major.encode('utf-8')))

    return majors


