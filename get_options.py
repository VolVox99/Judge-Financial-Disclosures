# import requests
# import json
# from fields import *


# def find_val(d, key):
#     s = json.dumps(d)
#     try:
#         start = s.index(key)
#     except:
#         return ''
#     try:
#         help_start = s.index("'help_text':", start) + len('"help_text":')
#         str_start = s.index("'", help_start) + 1
#         str_end = s.index("'", str_start)
#     except:
#         help_start = s.index('"help_text":', start) + len('"help_text":')
#         str_start = s.index('"', help_start) + 1
#         str_end = s.index('"', str_start)
        
#     ret = s[str_start: str_end]
#     return ret

    

# fin_disc = requests.options('https://www.courtlistener.com/api/rest/v3/financial-disclosures/')

# dic = disc_fields
# disc_field_keys_our = [i['name'] for key in disc_fields.keys() for i in disc_fields[key]]

# find_disc_data = fin_disc.json()['actions']['POST']

# d = {}
# for k in disc_field_keys_our:
#     v = find_val(find_disc_data, k)
#     # for _k in dic:
#     #     if _k['name'] == k:
#     #         k = _k.get('displayName') or _k.get('name')
    
    
#     d[k] = v


# with open('flattened_disc.json', 'w') as f:
#     f.write(json.dumps(d))
    
# for k, v in d.items():
    
#     print(f'{k}: {v}')

# # person_data = person.json()['actions']['PUT']

# # print(':\n'.join(disc_field_keys_our))
import requests
import json
from fields import *


def find_val(d, key, sub_sect = ''):
    
    s = json.dumps(d)
    try:
        abs_start = s.index(sub_sect)
        start = s.index(key, abs_start)
        
    except:
        return ''
    try:
        help_start = s.index("'help_text':", start) + len('"help_text":')
        str_start = s.index("'", help_start) + 1
        str_end = s.index("'", str_start)
    except:
        help_start = s.index('"help_text":', start) + len('"help_text":')
        str_start = s.index('"', help_start) + 1
        str_end = s.index('"', str_start)
        
    ret = s[str_start: str_end]
    return ret

    

fin_disc = requests.options('https://www.courtlistener.com/api/rest/v3/financial-disclosures/')

dic = disc_fields
disc_field_keys_our = [i['name'] for key in disc_fields.keys() for i in disc_fields[key]]

find_disc_data = fin_disc.json()['actions']['POST']

d = {}
for k in dic:
    print(f'\n{k}: ')
    for item in dic[k]:
        item = item['name']
        v = find_val(find_disc_data, item, sub_sect = k)
        print(f'\t{item}: {v} ')
        
        

# with open('flattened_disc.json', 'w') as f:
#     f.write(json.dumps(d))
    

   

# person_data = person.json()['actions']['PUT']

# print(':\n'.join(disc_field_keys_our))