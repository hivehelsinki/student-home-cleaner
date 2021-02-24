import os
import subprocess
import yaml

from tools.intra import ic
from datetime import date
from dateutil.relativedelta import relativedelta
from loguru import logger

logger.add("logs/logs.log", level="INFO", rotation="500 MB", retention="10 days", compression="zip")

with open('config.yml', 'r') as cfg_stream:
    config = yaml.load(cfg_stream, Loader=yaml.BaseLoader)

inactive_duration_month = int(config["inactive_duration_month"])


def _get(payload):
    data = ic.pages_threaded("cursus_users", params=payload)
    return [i['user']['login'] for i in data]


def _get_inactive():
    logger.debug(f"Get inactive students for less than {inactive_duration_month} months in campus_id: {config['campus_id']}")
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

def _get_active():
    logger.debug(f"Get active students in campus_id: {config['campus_id']}")
    payload = {
        'filter[campus_id]' : config['campus_id'],
        'filter[active]' : 'true',
    }
    
    return _get(payload)

def _delete(login):
    arg = f"./scripts/./delete_iscsi_home.sh {config['home_dir']} {login}"
    rc = subprocess.getstatusoutput(arg)
    if rc[0] == 0:
        logger.info(f"{arg} => rc: {rc[0]} ({rc[1]})")
    else: 
        logger.error(f"{arg} => rc: {rc[0]} ({rc[1]})")


def get_students():
    return list(set(_get_active() + _get_inactive() + config['allowed_list']))

def get_homes():
    logger.debug(f"Gather image files in: {config['home_dir']}")
    try:
        files = os.listdir(config['home_dir'])
        homes = [file.replace('.img', '') for file in files if file.endswith(".img")]
    except Exception as e:
        logger.error(f"error while gathering student homes list: {e}")
        exit(1)
    
    return homes

def delete_homes(logins):
    for login in logins:
        _delete(login)

