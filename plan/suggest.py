

def suggest_plan(choices):
  science = 1
  math = 2
  humanities = 3
  behavioral = 4
  business = 5
  art = 6
  health = 7
  choice = ['http://catalog.csun.edu/academics/phys/programs/bs-physics-i/physics/',
    'http://catalog.csun.edu/academics/math/programs/bs-mathematics-i/mathematics/',
    'http://catalog.csun.edu/academics/jour/programs/ba-journalism/',
    'http://catalog.csun.edu/academics/psy/programs/ba-psychology-i/',
    'http://catalog.csun.edu/academics/fin/programs/bs-finance-ii/financial-planning/',
    'http://catalog.csun.edu/academics/art/programs/ba-art/',
    'http://catalog.csun.edu/academics/hsci/programs/bs-public-health/']
  combo = ['http://catalog.csun.edu/academics/comp/programs/bs-computer-science/',
    'http://catalog.csun.edu/academics/hsci/programs/bs-health-administration/']
  if len(choices) == 1 :
    return choice[choices[0]]
  else:
    if science in choices and math in choices:
      return combo[0]
    elif business in choices and health in choices:
      return combo[1]
    else:
      return choice[choices[0]]

# print suggest_plan([1])
# print suggest_plan([0,1])
# print suggest_plan([1,4,6])
# print suggest_plan([3,4,5])
