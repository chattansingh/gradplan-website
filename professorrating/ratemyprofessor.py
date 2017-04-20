import os, urllib2, json
from bs4 import BeautifulSoup
from professorrating.models import Professor, ClassRating


def update_db_rmp_professor_names_urls(json_file_name, **kwargs):
    url_list = kwargs.pop('url_list', None)
    if url_list:
        print "URL list provided.."
        opener = urllib2.build_opener()
        for url in url_list:
            url = url.encode('utf-8')
            external_sites_html = opener.open(url).read()
            name = BeautifulSoup(external_sites_html, 'html.parser').find('div', attrs={"class": "name"}).text.encode('utf-8')
            if name:
                split = name.split()
                try:
                    first_name = split[0]
                    last_name = split[1]
                except IndexError:
                    if len(split) == 1:
                        first_name = split[0]
                        last_name = 'N/A'
                    else:
                        first_name = 'No First Name Found'
                        last_name = 'No Last Name Found'
                prof, created = Professor.objects.update_or_create(last_name=last_name, first_name=first_name, rmp_url=url)
                # prof_name_url.append({'prof_last_name': last_name, 'prof_first_name' : first_name, 'url': url})
                if created:
                    print 'Created: ' + last_name + ', ' + first_name + ' rmp url: ' + url
                else:
                    print 'Updated: ' + last_name + ', ' + first_name + ' rmp url: ' + url
                prof.save()
            else:
                print "[*] Name: " + ".  Profesor at url: " + url + " was not added."
    else:
        print '[*] Getting urls from json files...'
        dir = '/Users/evance/OneDrive/School/Year_2016-17/Spring_2017/comp_680/software/gradplan-website/professorrating/' + json_file_name
        file = os.path.expanduser(dir)
        with open(file, 'r') as json_file:
            json_data = json.load(json_file)
            json_list = [prof['url'].decode('utf-8') for prof in json_data]

        print "finished opening .json file....\nbeginning to parse urls and get html title..."
        # prof_name_url = []
        opener = urllib2.build_opener()
        for url in json_list:
            external_sites_html = opener.open(url).read()
            title = BeautifulSoup(external_sites_html, 'html.parser').title.string
            split = title.split()
            first_name = split[0]
            last_name = split[1]
            prof, created = Professor.objects.update_or_create(last_name=last_name, first_name=first_name, rmp_url=url)
            # prof_name_url.append({'prof_last_name': last_name, 'prof_first_name' : first_name, 'url': url})
            if created:
                print 'Created: ' + last_name + ', ' + first_name + ' rmp url: ' + url
            else:
                print 'Updated: ' + last_name + ', ' + first_name + ' rmp url: ' + url
            prof.save()

def clear_rating_data(first_name, last_name):
    prof = Professor.objects.get(first_name=first_name, last_name=last_name)
    prof.average_rating = 0
    prof.number_of_ratings = 0
    prof.total_rating = 0
    ratings = ClassRating.objects.filter(professor=prof)
    for rating in ratings:
        rating.delete()
    prof.save()