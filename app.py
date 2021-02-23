from tools.intra import ic
from datetime import date
from dateutil.relativedelta import relativedelta
import yaml
import os

with open('config.yml', 'r') as cfg_stream:
    config = yaml.load(cfg_stream, Loader=yaml.BaseLoader)

inactive_duration_month = int(config["inactive_duration_month"])


def _get(payload):
    data = ic.pages_threaded("cursus_users", params=payload)
    return [i['user']['login'] for i in data]


def get_inactive():
    since = (
        date.today() - relativedelta(months=inactive_duration_month)
    ).strftime("%Y-%m-%dT%H:%M:%S")
    interval = since + ',' + date.today().strftime("%Y-%m-%dT%H:%M:%S")

    payload = {
        'filter[campus_id]' : config['campus_id'],
        'filter[active]' : 'false',
        'range[end_at]' : interval
    }
    return _get(payload)

def get_active():
    payload = {
        'filter[campus_id]' : config['campus_id'],
        'filter[active]' : 'true',
    }
    
    return _get(payload)

def main():
    students = list(
        set(get_active() + get_inactive() + config['allowed_list'])
    )

    files = os.listdir(config['home_dir'])
    homes = [file.replace('.img', '') for file in files if file.endswith(".img")]

    print(list(set(homes) - set(students)))
    # students = ', '.join(map(str, students))
    # # with open("students.txt", 'w') as f:
    # #     f.write(students)
    # #     f.close()
    # return list(students)


if __name__ == "__main__":
    main()