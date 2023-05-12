from calendar import day_abbr
import sys
import datetime
from turtle import position
import time
from datetime import datetime
from datetime import date
from datetime import timedelta
from unicodedata import name
from urllib.parse import _NetlocResultMixinStr

sys.path.append("/usr/local/lib/python3.9/site-packages")
sys.path.insert(0,'./')
sys.path.insert(0,'/usr/local/lib/python3.9/site-packages')
sys.path.append("..")
import pypco
import pytz

pco_update_list = []


PCO_APPLICATION_KEY = "3f388f771fc65883abb3200a2bf956ec14a15f6b2283b34899f9d58f20cfb475"
PCO_API_SECRET = "da13f98d600ac7319e9a5f26750bd2649bc00ba04b9883daa4b24057b52a3d42"
pco = pypco.PCO(PCO_APPLICATION_KEY, PCO_API_SECRET)
attachment_list = []
next_upcoming_plan = {}
service_types = {}
allowed_service_types = {'Sunday AM','Sunday PM','Wednesday PM','THIS IS ONLY A TEST'}
allowed_team_ids = {'3291057','3294972','3294977','3294979'}
nowPlus = date.today() + timedelta(days=6)
now = nowPlus.strftime("%Y-%m-%dT%H:%M:%S%z")


def pco_json_mini(self):
    slot = self['slot']
    name = self['name']
    return {
        'slot': slot,
        'name': name,
        'timestamp': time.time()
    }

def getServiceTypes():
    service_types = pco.iterate('/services/v2/service_types')
    service_types = [service_type for service_type in service_types if service_type['data']['attributes']['name'] in allowed_service_types]
    return service_types

def getUpcomngPlan():
    utc = pytz.UTC
    today = utc.localize(datetime.now())
    service_types = getServiceTypes()
    next_upcoming_plan = {}
    for service_type in service_types:
        raw_plans = pco.iterate('/services/v2/service_types/' + service_type['data']['id'] + '/plans', filter='future', order='sort_date', include='plan_times')
        for raw_plan in raw_plans:
            service_length = raw_plan['data']['attributes']['total_length']
            service_length = service_length + 300
            sort_date =  datetime.strptime(raw_plan['data']['attributes']['sort_date'],'%Y-%m-%dT%H:%M:%S%z')
            end_date = sort_date + timedelta(seconds=service_length)
            if next_upcoming_plan:
                next_date = datetime.strptime(next_upcoming_plan['data']['attributes']['sort_date'], '%Y-%m-%dT%H:%M:%S%z')
                if sort_date < next_date:
                    if end_date > today:
                        next_upcoming_plan = raw_plan

            else:
                if end_date > today:
                    next_upcoming_plan = raw_plan
    return next_upcoming_plan


def getTeamMembers(slot):
    upcoming_plan = getUpcomngPlan()
    assigned_team_members = pco.iterate('/services/v2/service_types/' + upcoming_plan['data']['relationships']['service_type']['data']['id'] + '/plans/' + upcoming_plan['data']['id'] + '/team_members',filter='confirmed')

    assigned_team_members = [assigned_member for assigned_member in assigned_team_members if assigned_member['data']['relationships']['team']['data']['id'] in allowed_team_ids]

    intNumber = 1
    vocals = {}
    for vocal_team_member in assigned_team_members:
        if slot == intNumber:
            # vocalString = str(intNumber) + '-' + vocal_team_member['data']['attributes']['name']
            name=vocal_team_member['data']['attributes']['name']
            newvocal={name:intNumber}
            vocals.update(newvocal)
            intNumber = intNumber + 1
        else:
            intNumber = intNumber + 1
        
    return vocals

def getTeam():
    upcoming_plan = getUpcomngPlan()
    assigned_team_members = pco.iterate('/services/v2/service_types/' + upcoming_plan['data']['relationships']['service_type']['data']['id'] + '/plans/' + upcoming_plan['data']['id'] + '/team_members',filter='confirmed')

    assigned_team_members = [assigned_member for assigned_member in assigned_team_members if assigned_member['data']['relationships']['team']['data']['id'] in allowed_team_ids]

    vocals = []
    for vocal_team_member in assigned_team_members:
            # vocalString = str(intNumber) + '-' + vocal_team_member['data']['attributes']['name']
            name=vocal_team_member['data']['attributes']['name']
            pcoPosition = vocal_team_member['data']['attributes']['team_position_name']
            mic_number = [int(s) for s in str.split(pcoPosition) if s.isdigit()]
            if mic_number:
                newvocal={'slot':mic_number[0], 'name':name}
                vocals.append(newvocal)
                if newvocal not in pco_update_list:
                    pco_update_list.append(newvocal)

    return vocals

