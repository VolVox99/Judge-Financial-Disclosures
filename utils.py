import auth_token
import fields
from time import sleep
from requests import get
from lookups import *
from tqdm import tqdm

def req(url):
    headers = {
        'Authorization': f'Token {auth_token.token}'
    }
    try:
        res = get(url, headers = headers)
        return res.json()
    #retry
    except:
        sleep(2.5)
        res = get(url, headers = headers)
        return res.json()


def apply_lookup(val, field):
    lookups = field.get('lookup', [])
    for lookup in lookups:
        if lookup['value'] == val:
            return lookup['display_name']
        
    return val
    

def get_person_fields(person):
    person_info = req(person['person'])
    
    d = {}
    for field in fields.person_fields:
        key = field.get('displayName') or field['name']
        if 'get' in field:
            val = field['get'](person_info)
        else:
            val = person_info.get(field['name'])
        val = apply_lookup(val, field)
        d[key] = val
        
    return d

def get_common_fields(all_data):
    d = {}
    for field in fields.common_fields:
        key =  field.get('displayName') or field['name']
        v = all_data[field['name']]
        v = apply_lookup(v, field)
        d[key] = v

    return d

def generate_max_field(field):
    return field + '_max'

def is_code_field(field):
    return field.endswith('_code')

def get_code_maxes(row):
    ret = {k:'' for k in fields.code_max_field_keys}
    for field, value in row.items():
        if is_code_field(field):
            k = generate_max_field(field)
            #will be '25,000,001 - 50,000,000' || '50,000,001 - '
            #remove whitespace, split and remove empty string to handle second value
            try:
                v = [i.strip() for i in value.split('-') if i.strip()][-1]
            except IndexError:
                v = ''
            ret[k] = v
        
    return ret

def get_disclosure_fields(disc, disc_type):
    row = {} 
    
    for field in fields.disc_fields[disc_type]:
        k = field['name']
        v = disc[k]
        v = apply_lookup(v, field)
        row[k] = v
        
    return row | get_code_maxes(row)


def get_position_fields(url):
    res = req(url)
    
    #private job
    if res['job_title']:
        return f"{res['job_title']} for {res['organization_name']} {res['date_start']} to {res['date_termination']} in {res['location_city']}, {res['location_state']}".replace('None', 'N/A')

    #court position
    elif res['position_type']:
        return f"{res['position_type']} for {res['court']['full_name']}".replace('None', 'N/A')
    
    return ''


def sleep_progress(secs):
    for _ in tqdm(range(secs)):
        sleep(1)