

def suggest_plan(choices):
  science = 1
  math = 2
  humanities = 3
  behavioral = 4
  business = 5
  art = 6
  health = 7
  choice = ['Physics: Physics, B.S.',
    'Mathematics: Mathematics, B.S.',
    'Journalism, B.A.',
    'Psychology, B.A.',
    'Finance: Financial Planning, B.S.',
    'Art, B.A.',
    'Public Health, B.S.']
  combo = ['Computer Science, B.S.',
    'Health Administration, B.S.']
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
