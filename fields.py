from lookups import *
from utils import get_position_fields, is_code_field, generate_max_field


def error_decorator(func, err = ''):
    def new_func(*args, **kwargs):
        try:
            return func(*args, **kwargs) or err
        except Exception as e:
            print('ERROR:', e)
            return err
    
    return new_func


#fields to grab from each disclosure type
disc_fields = {
    "agreements": [
        {"name": "date_raw"},
        {"name": "parties_and_terms"},
        {"name": "redacted"},
        {"name": "financial_disclosure"},
        {"name": "id"},
        {"name": "date_created"},
        {"name": "date_modified"},
    ],
    "debts": [
        {"name": "creditor_name"},
        {"name": "description"},
        {
            "name": "value_code",
            "lookup": [
                {"value": "J", "display_name": "1 - 15,000"},
                {"value": "K", "display_name": "15,001 - 50,000"},
                {"value": "L", "display_name": "50,001 - 100,000"},
                {"value": "M", "display_name": "100,001 - 250,000"},
                {"value": "N", "display_name": "250,001 - 500,000"},
                {"value": "O", "display_name": "500,001 - 1,000,000"},
                {"value": "P1", "display_name": "1,000,001 - 5,000,000"},
                {"value": "P2", "display_name": "5,000,001 - 25,000,000"},
                {"value": "P3", "display_name": "25,000,001 - 50,000,000"},
                {"value": "P4", "display_name": "50,000,001 - "},
                {"value": "-1", "display_name": "Failed Extraction"},
            ],
        },
        {"name": "redacted"},
        {"name": "id"},
        {"name": "date_created"},
        {"name": "date_modified"},
    ],
    "gifts": [
        {"name": "source"},
        {"name": "description"},
        {"name": "value"},
        {"name": "redacted"},
        {"name": "id"},
        {"name": "date_created"},
        {"name": "date_modified"},
    ],
    "investments": [
        {"name": "page_number"},
        {"name": "description"},
        {"name": "redacted"},
        {
            "name": "income_during_reporting_period_code",
            "lookup": [
                {"value": "A", "display_name": "1 - 1,000"},
                {"value": "B", "display_name": "1,001 - 2,500"},
                {"value": "C", "display_name": "2,501 - 5,000"},
                {"value": "D", "display_name": "5,001 - 15,000"},
                {"value": "E", "display_name": "15,001 - 50,000"},
                {"value": "F", "display_name": "50,001 - 100,000"},
                {"value": "G", "display_name": "100,001 - 1,000,000"},
                {"value": "H1", "display_name": "1,000,001 - 5,000,000"},
                {"value": "H2", "display_name": "5,000,001  "},
                {"value": "-1", "display_name": "Failed Extraction"},
            ],
        },
        {"name": "income_during_reporting_period_type"},
        {
            "name": "gross_value_code",
            "lookup": [
                {"value": "J", "display_name": "1 - 15,000"},
                {"value": "K", "display_name": "15,001 - 50,000"},
                {"value": "L", "display_name": "50,001 - 100,000"},
                {"value": "M", "display_name": "100,001 - 250,000"},
                {"value": "N", "display_name": "250,001 - 500,000"},
                {"value": "O", "display_name": "500,001 - 1,000,000"},
                {"value": "P1", "display_name": "1,000,001 - 5,000,000"},
                {"value": "P2", "display_name": "5,000,001 - 25,000,000"},
                {"value": "P3", "display_name": "25,000,001 - 50,000,000"},
                {"value": "P4", "display_name": "50,000,001 - "},
                {"value": "-1", "display_name": "Failed Extraction"},
            ],
        },
        {
            "name": "gross_value_method",
            "lookup": [
                {"value": "Q", "display_name": "Appraisal"},
                {"value": "R", "display_name": "Cost (Real Estate Only)"},
                {"value": "S", "display_name": "Assessment"},
                {"value": "T", "display_name": "Cash Market"},
                {"value": "U", "display_name": "Book Value"},
                {"value": "V", "display_name": "Other"},
                {"value": "W", "display_name": "Estimated"},
                {"value": "-1", "display_name": "Failed Extraction"},
            ],
        },
        {"name": "transaction_during_reporting_period"},
        {"name": "transaction_date_raw"},
        {"name": "transaction_date"},
        {
            "name": "transaction_value_code",
            "lookup": [
                {"value": "J", "display_name": "1 - 15,000"},
                {"value": "K", "display_name": "15,001 - 50,000"},
                {"value": "L", "display_name": "50,001 - 100,000"},
                {"value": "M", "display_name": "100,001 - 250,000"},
                {"value": "N", "display_name": "250,001 - 500,000"},
                {"value": "O", "display_name": "500,001 - 1,000,000"},
                {"value": "P1", "display_name": "1,000,001 - 5,000,000"},
                {"value": "P2", "display_name": "5,000,001 - 25,000,000"},
                {"value": "P3", "display_name": "25,000,001 - 50,000,000"},
                {"value": "P4", "display_name": "50,000,001 - "},
                {"value": "-1", "display_name": "Failed Extraction"},
            ],
        },
        {
            "name": "transaction_gain_code",
            "lookup": [
                {"value": "A", "display_name": "1 - 1,000"},
                {"value": "B", "display_name": "1,001 - 2,500"},
                {"value": "C", "display_name": "2,501 - 5,000"},
                {"value": "D", "display_name": "5,001 - 15,000"},
                {"value": "E", "display_name": "15,001 - 50,000"},
                {"value": "F", "display_name": "50,001 - 100,000"},
                {"value": "G", "display_name": "100,001 - 1,000,000"},
                {"value": "H1", "display_name": "1,000,001 - 5,000,000"},
                {"value": "H2", "display_name": "5,000,001 - "},
                {"value": "-1", "display_name": "Failed Extraction"},
            ],
        },
        {"name": "transaction_partner"},
        {"name": "has_inferred_values"},
        {"name": "id"},
        {"name": "date_created"},
        {"name": "date_modified"},
    ],
    "non_investment_incomes": [
        {"name": "date_raw"},
        {"name": "source_type"},
        {"name": "income_amount"},
        {"name": "redacted"},
        {"name": "id"},
        {"name": "date_created"},
        {"name": "date_modified"},
    ],
    "positions": [
        {"name": "position", "displayName": "non judiciary position"},
        {"name": "organization_name"},
        {"name": "redacted"},
        {"name": "id"},
        {"name": "date_created"},
        {"name": "date_modified"},
    ],
    "reimbursements": [
        {"name": "source"},
        {"name": "date_raw"},
        {"name": "location"},
        {"name": "purpose"},
        {"name": "items_paid_or_provided"},
        {"name": "redacted"},
        {"name": "id"},
        {"name": "date_created"},
        {"name": "date_modified"},
    ],
    "spouse_incomes": [
        {"name": "id"},
        {"name": "date_created"},
        {"name": "date_modified"},
        {"name": "source_type"},
        {"name": "redacted"},
        {"name": "date_raw"},
    ]
}


#fields to grab from the person
person_fields = [
    {
        'name': 'race',
        'get': lambda p: ','.join([race_lookup[i] for i in p['race']]),
    },
    {
        'name': 'fjc_id'
    },
    {
        'name': 'cl_id'
    },
    {
        'name': 'name_first'
    },
    {
        'name': 'name_middle'
    },
    {
        'name': 'name_last'
    },
    {
        'name': 'name_suffix',
        'lookup':  [
            {
                "value": "jr",
                "display_name": "Jr."
            },
            {
                "value": "sr",
                "display_name": "Sr."
            },
            {
                "value": "1",
                "display_name": "I"
            },
            {
                "value": "2",
                "display_name": "II"
            },
            {
                "value": "3",
                "display_name": "III"
            },
            {
                "value": "4",
                "display_name": "IV"
            }
        ]
    },
    {
        'name': 'date_dob',
        'displayName': 'Date of Birth'
    },
    {
        'name': 'date_dod',
        'displayName': 'Date of Death'
    },
    {
        'name': 'dob_city',
        'displayName': 'Birth City'
    },
    {
        'name': 'dob_state',
        'displayName': 'Birth State',
        
    },
    {
        'name': 'dob_country',
        'displayName': 'Birth Country'
    },
    {
        'name': 'dod_city',
        'displayName': 'Death City'
    },
        {
        'name': 'dod_state',
        'displayName': 'Death State',
    },
    {
        'name': 'dod_country',
        'displayName': 'Death Country'
    },
    {
        'name': 'gender',
        'lookup':  [
                    {
                        "value": "m",
                        "display_name": "Male"
                    },
                    {
                        "value": "f",
                        "display_name": "Female"
                    },
                    {
                        "value": "o",
                        "display_name": "Other"
                    }
                ]
    },
    {
        'name': 'religion',
    },
    {
        'name': 'ftm_total_received',
    },
    {
        'name': 'ftm_eid',
    },
    {
        'name': 'sources',
        'displayName': 'sources',
        'get': lambda p: '\n'.join([i.get('url', '') for i in p['sources']])
    },
    {
        'name': 'aba_ratings',
        'get': lambda p: ','.join([f"{aba_ratings_lookup.get(i['rating'], '')} - {i.get('year_rated', '')}".replace('None', 'N/A') for i in p['aba_ratings']])
    },
    {
        'name': 'educations',
        'get': lambda p: ','.join([f"{degrees_lookup.get(i['degree_level'], '')} - {i['school']['name']}".replace('None', 'N/A') for i in p['educations']])
    },
    {
        'name': 'bachelor school',
        'get': lambda p: ','.join([i['school']['name'] for i in p['educations'] if i['degree_level'] in ('ba','llb')])
    },
    {
        'name': 'juris doctor school',
        'get': lambda p: ','.join([i['school']['name'] for i in p['educations'] if i['degree_level'] =='jd'])
    },
    {
        'name': 'positions',
        'get': lambda p: '\n'.join([get_position_fields(i) for i in p['positions']])
    },
    {
        'name': 'political_affiliations',
        'get': lambda p: ','.join([f"{political_party_lookup[i['political_party']]} from {political_source_lookup[i['source']]}".replace('None', 'N/A') for i in p['political_affiliations']])
    },
    
    
]

#fields common to disclosure report
common_fields = [
    {
        'name': 'year',
        'displayName': 'Year Disclosed'
    },
    {
        'name': 'report_type',
        'lookup': [
            {
                "value": -1,
                "display_name": "Unknown Report"
            },
            {
                "value": 0,
                "display_name": "Nomination Report"
            },
            {
                "value": 1,
                "display_name": "Initial Report"
            },
            {
                "value": 2,
                "display_name": "Annual Report"
            },
            {
                "value": 3,
                "display_name": "Final Report"
            }
        ]
    },
    {
        'name': 'is_amended'
    },
    {
        'name': 'addendum_redacted'
    },
    {
        'name': 'filepath',
        'displayName': 'Disclosure PDF'
    },
    {
        'name': 'sha1',
        'displayName': 'Disclosure PDF'
    }
]

for element in person_fields:
    if 'get' in element:
        element['get'] = error_decorator(element['get'], element.get('errorVal'))


disc_types = list(disc_fields.keys())
disc_field_keys = [i.get('displayName', i['name']) for key in disc_fields.keys() for i in disc_fields[key]]
person_field_keys = [i.get('displayName', i['name']) for i in person_fields]
common_field_keys = [i.get('displayName', i['name']) for i in common_fields] + ['Disclosure Type']
code_max_field_keys = [generate_max_field(i) for i in disc_field_keys if is_code_field(i)]

#combine and remove duplicates
all_field_names = list(set(disc_field_keys + person_field_keys + common_field_keys + code_max_field_keys))