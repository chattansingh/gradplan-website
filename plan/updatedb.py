'''
    Model of the output
    [
        {'major': u'Urban Studies and Planning, B.A.', 
        
        'plan': '[
                    {"classes": [
                                    {"dept": "GE", "prereqs": [], "number": "Basic Skills: Written Communication"}, 
                                    {"dept": "GE", "prereqs": [], "number": "Basic Skills: Critical Thinking"}, 
                                    {"dept": "GE", "prereqs": [], "number": "Basic Skills: Mathematics"}, 
                                    {"dept": "GE", "prereqs": [], "number": "Basic Skills: Oral Communication"}
                                ]
                    }, 
                    {"classes": [
                                    {"dept": "GE", "prereqs": [], "number": "Natural Science "}, 
                                    {"dept": "GE", "prereqs": [], "number": "Arts and Humanities"}
                                ]
                    }, 
                    {"classes": [
                                    {"dept": "GE", "prereqs": [], "number": "Social Sciences"}, 
                                    {"dept": "GE", "prereqs": [], "number": "Lifelong Learning"}, 
                                    {"dept": "GE", "prereqs": [], "number": "Natural Science "}, 
                                    {"dept": "URBS", "prereqs": [], "number": ["206"]}
                                ]
                    }, 
                    {"classes": [
                                    {"dept": "GE", "prereqs": [], "number": "Comparative Cultures"}, 
                                    {"dept": "Title", "prereqs": [], "number": "5 Requirement"}, 
                                    {"dept": "Title", "prereqs": [], "number": "5 Requirement"}, 
                                    {"dept": "URBS", "prereqs": [], "number": ["250"]}
                                ]
                    }, 
                    {"classes": [
                                    {"dept": "URBS", "prereqs": [], "number": ["310"]}, 
                                    {"dept": "URBS", "prereqs": [], "number": ["340A"]}, 
                                    {"dept": "GE", "prereqs": [], "number": "Upper Division Arts and Humanities"}
                                ]
                    }, 
                    {"classes": [
                                    {"dept": "URBS", "prereqs": [], "number": ["340B"]}, 
                                    {"dept": "URBS", "prereqs": [], "number": ["300"]}]
                    }, 
                    {"classes": [
                                    {"dept": "URBS", "prereqs": [], "number": ["440"]}, 
                                    {"dept": "URBS", "prereqs": [], "number": ["490C"]}
                                ]
                    }, 
                    {"classes": [
                                    {"dept": "URBS", "prereqs": [], "number": ["494C"]}, 
                                    {"dept": "URBS", "prereqs": [], "number": ["450"]}, 
                                    {"dept": "URBS", "prereqs": [], "number": ["460"]}, 
                                    {"dept": "GE", "prereqs": [], "number": "Upper Division Comparative Cultures "}
                                ]
                    }
                ]'
        }
    ]
    
    
    mr = MajorRoadMaps.objects.update_or_create(major=)
'''

from plan.models import MajorRoadMaps
from plan.gradplan import getbaseplans
import json


def update_database(**kwars):
    print "Updating the graduation plan database..."
    plans = kwars.pop('plans', None)
    if plans:
        print "Argument supplied...\nSkiping the url scrapping..."
        for p in plans:
            p['major'] = p['major'].encode('utf-8')
        for p in plans:
            major = p['major']
            road_map = p['plan']
            major_road_map, created = MajorRoadMaps.objects.update_or_create(major=major, road_map=road_map)
            output_status(major, created)
            major_road_map.save()
    else:
        print "No Argument supllied...\nGetting gradutation plans"
        plans = getbaseplans()
        for p in plans:
            p['major'] = p['major'].encode('utf-8')
        for p in plans:
            major = p['major']
            road_map = p['plan']
            major_road_map, created = MajorRoadMaps.objects.update_or_create(major=major, road_map=road_map)
            output_status(major, created)
            major_road_map.save()

def output_status(major, created):
    if created:
        print "Created: " + major + "grad plan."
    else:
        print "Updated: " + major + "grad plan."

def test_database():
    major_road_map = MajorRoadMaps.objects.get(major='Urban Studies and Planning, B.A.')
    print major_road_map