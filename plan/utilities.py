#various utilites to format the plan

def get_prof_email_name(email):
    #takes the professors email and returns the first and last name on the email
    #hopefully only returns only first or last if in form first@csun.edu or last@csun.edu
    try:
        return [p.capitalize() for p in email.split('@')[0].split('.')]
    except IndexError:
        return []