"""Module to hold lengthy sets/dictionaries used to check user inputs in tidyhome.py"""

state_set = {
    'AL',
    'AK',
    'AZ',
    'AR',
    'CA',
    'CO',
    'CT',
    'DE',
    'DC',
    'FL',
    'GA',
    'HI',
    'ID',
    'IL',
    'IN',
    'IA',
    'KS',
    'KY',
    'LA',
    'ME',
    'MD',
    'MA',
    'MI',
    'MN',
    'MS',
    'MO',
    'MT',
    'NE',
    'NV',
    'NH',
    'NJ',
    'NM',
    'NY',
    'NC',
    'ND',
    'OH',
    'OK',
    'OR',
    'PA',
    'RI',
    'SC',
    'SD',
    'TN',
    'TX',
    'UT',
    'VT',
    'VA',
    'WA',
    'WV',
    'WI',
    'WY',
    'AS',
    'GU',
    'MP',
    'PR',
    'VI',
    'UM',
    'FM',
    'MH',
    'PW',
}

#Keys match Enum value (ie. Race.Asian.value == 0 | '0' : 'Asian')
race_dictionary = {
    0 : 'Asian',
    1 : 'Native Hawaiian or Other Pacific Islander',
    2 : 'Free Form Text Only',
    3 : 'Race Not Available',
    4 : 'American Indian or Alaska Native', 
    5 : 'Black or African American', 
    6 : '2 or more minority races', 
    7 : 'White', 
    8 : 'Joint'   
}