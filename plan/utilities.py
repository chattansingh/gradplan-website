#various utilites
from plan.models import MajorRoadMaps
import json


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


def update_detail_sem(detail_sem):
    for sem in detail_sem['classes']:
        for detail in sem['details']:
            for prof in detail['instructors']:
                prof_email = prof['instructor']
                first_last = get_prof_email_name(prof_email)
                if len(first_last) > 1:
                    first_last = {'first_name': first_last[0], 'last_name': first_last[1]}
                else:
                    first_last = {'first_name': first_last[0], 'last_name': ''}
                prof.update(first_last)
    return detail_sem

def get_semester(road_map):

    # list of classes
    try:
        road_map = json.loads(road_map)
    except TypeError or ValueError:
        pass
    detail_sem = road_map[0]
    remaining_sem = road_map[1:]
    remaining_sem = [sem['classes'] for sem in remaining_sem]
    dict = update_detail_sem(detail_sem)
    return {'detail_sem': dict, 'remaining_sem':remaining_sem}

def get_common_classes(majors_chosen):

    if majors_chosen:
        majors = []

        for major in majors_chosen:
            try:
                semester = json.loads(major)[0]
            except TypeError or ValueError:
                semester = major[0]
            majors.append([c['dept'] + c['number'] for c in semester['classes']])

        result = list(set.intersection(*map(set, majors)))
        try:
            detail_sem =  {'classes' : [item  for item in json.loads(majors_chosen[0])[0]['classes'] if item['dept']+item['number'] in result]}
        except TypeError or ValueError:
            detail_sem = {'classes': [item for item in majors_chosen[0][0]['classes'] if
                                      item['dept'] + item['number'] in result]}
        return update_detail_sem(detail_sem)