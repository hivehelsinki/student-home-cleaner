from tools.intra import ic
from datetime import date
from dateutil.relativedelta import relativedelta
import yaml

# Get students from endpoint with params
def get_students(endpoint, params):
    students = []
    data = ic.pages_threaded(endpoint, params=params)
    for item in data:
        students.append(item['user']['login'])
    return students

def get_active_students():
    # Get allowed_list from .yml file
    with open('cleaner.yml', 'r') as cfg_stream:
        config = yaml.load(cfg_stream, Loader=yaml.BaseLoader)
    allowed_list = config['allowed_list']

     # endpoint and time for now/last_month
    endpoint = "cursus_users"
    now = date.today().strftime("%Y-%m-%dT%H:%M:%S")
    since = (date.today() + relativedelta(months=-1)).strftime("%Y-%m-%dT%H:%M:%S")
    last_month = since + ',' + now

    # Hive student with inactive cursus in last month
    params = {
        'filter[campus_id]' : 13,
        'filter[active]' : 'false',
        'range[end_at]' : last_month
    }
    inactives = get_students(endpoint, params)

    # Active Hive students
    params = {
        'filter[campus_id]' : 13,
        'filter[active]' : 'true',
    }
    actives = get_students(endpoint, params)
    
    # Turn actives and inactives into set to remove duplicates
    students = set(actives + inactives)

    # Remove allowed users from the list
    for user in allowed_list:
        if user in students:
            students.remove(user)

    # Write to a file
    students = ', '.join(map(str, students))

    with open("students.txt", 'w') as f:
        f.write(students)
        f.close()

    #return list(students)

get_active_students()

