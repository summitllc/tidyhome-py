"""This module assists with the process of retrieving data from the CFPB'S HDMA API.

Tidyhome provides users with functions that make a single request to the HDMA API and place the 
requested data in a pandas DataFrame. Two Enum classes ('Races' and 'Actions') have been created to 
help users more easily formulate valid API requests. When using a tidyhome function, the 'races' and 
'actions' parameters both expect an argument from their respective Enum class.

    Usage examples:

    tidyhome.get_institutions(2020, ['dc', 'md', 'va'])
    tidyhome.get_loans(2019, 'dc', [Action.INCOMPLETE, Action.PREAPPROVED], [Race.BLACK, Race.WHITE])
    tidyhome.get_aggregations(2018, 'dc' , races=Race.UNAVAILABLE)
"""
####################################
# AUTHOR: Summit Consulting LLC
# PURPOSE: To circumnavigate the HMDA API for entry-level data scientists
# NOTES:
#     https://cfpb.github.io/hmda-platform/#hmda-api-documentation
####################################

from typing import Dict, Iterable, List, Optional, Union
from enum import Enum
import pandas as pd
import requests
from check_dictionaries import state_set, race_dictionary

# Limit what gets imported via the 'import *' statement
__all__ = [
    'Race',
    'Action',
    'get_aggregations',
    'get_institutions',
    'get_loans'
]

class Race(Enum):
    """Enum class to simplify inputting valid 'races' parameter"""
    ASIAN = 0
    PACIFIC_ISLANDER = 1
    FREE_FORM = 2
    UNAVAILABLE = 3
    NATIVE_AMERICAN = 4
    BLACK = 5
    MIXED_MINORITY = 6
    WHITE = 7
    JOINT = 8

# Values correspond with actions recognized by HDMA API
class Action(Enum):
    """Enum class to simplify inputting valid 'actions_taken' parameter"""
    ORIGINATED = 1
    APPROVED = 2
    DENIED = 3
    WITHDRAWN = 4
    INCOMPLETE = 5
    PURCHASED = 6
    PREDENIED = 7
    PREAPPROVED = 8

### (Main functions) ###

def get_aggregations(years: int,
                     states: Union[str, List[str]],
                     actions: Optional[Union[Action, List[Action]]] = None,
                     races: Optional[Union[Race, List[Race]]] = None) -> pd.DataFrame:
    '''
    Get HDMA aggregate loan level data.

    Args:
        years (int): year in the range 2018-2020 (Only one year should be
            passed for each call, since the HDMA API can only show data for one
            year per request).

        states (str | List[str]): valid Two-Letter State Abbreviations for US
            state or territory.

        actions (Action | List[Action]): action(s) taken by population
            information is being requested for.

        races (Race | List[Race]): race(s) of population information is being
            requested for.

    Returns:
        pandas.DataFrame

    Raises:
        Exception: If HTTP request to API contains bad syntax or cannot be fulfilled.
    '''
    if not actions and not races:
        raise Exception("You must provide an argument to at least one of `actions` or `races`.")

    endpoint = "https://ffiec.cfpb.gov/v2/data-browser-api/view/aggregations"
    params= get_params(years, states, actions, races)
    response = requests.get(endpoint, params=params)

    if response.status_code != 200:
        raise Exception(response.text)

    response_json = response.json()
    parsed_json = response_json["aggregations"]
    data = pd.DataFrame(parsed_json)
    return data

def get_institutions(years: int,
                     states: Union[str, List[str]],
                     actions: Optional[Union[Action, List[Action]]] = None,
                     races: Optional[Union[Race, List[Race]]] = None) -> pd.DataFrame:
    '''
    Get HMDA data by filing institutions.

    Args:
        years (int): year in the range 2018-2020 (Only one year should be
            passed for each call, since the HDMA API can only show data for one
            year per request).

        states (str | List[str]): valid Two-Letter State Abbreviations for US
            state or territory.

        actions (Action | List[Action]): action(s) taken by population
            information is being requested for.

        races (Race | List[Race]): race(s) of population information is being
            requested for.

    Returns:
        pandas.DataFrame

    Raises:
        Exception: If HTTP request to API contains bad syntax or cannot be fulfilled.
    '''
    endpoint = "https://ffiec.cfpb.gov/v2/data-browser-api/view/filers"
    params = get_params(years, states, actions, races)
    response = requests.get(endpoint, params=params)

    if response.status_code != 200:
        raise Exception(response.text)

    response_json = response.json()
    parsed_json = response_json["institutions"]
    data = pd.DataFrame(parsed_json)
    return data

def get_loans(years: int,
              states: Union[str, List[str]],
              actions: Optional[Union[Action, List[Action]]] = None,
              races: Optional[Union[Race, List[Race]]] = None) -> pd.DataFrame:
    '''
    Get HMDA individual loan level data.

    Args:
        years (int): year in the range 2018-2020 (Only one year should be
            passed for each call, since the HDMA API can only show data for one
            year per request).

        states (str | List[str]): valid Two-Letter State Abbreviations for US
            state or territory.

        actions (Action | List[Action]): action(s) taken by population
            information is being requested for.

        races (Race | List[Race]): race(s) of population information is being
            requested for.

    Returns:
        pandas.DataFrame

    Raises:
        Exception: If HTTP request to API contains bad syntax or cannot be fulfilled.
    '''
    if not actions and not races:
        raise Exception("You must provide an argument to at least one of `actions` or `races`.")

    endpoint = "https://ffiec.cfpb.gov/v2/data-browser-api/view/csv"
    params = get_params(years, states, actions, races)
    response = requests.get(endpoint, params=params)

    if response.status_code != 200:
        raise Exception(response.text)

    data = pd.read_csv(response.url, low_memory=False)
    return data

### (Helper function for Main functions) Create API parameter dictionary ###

def get_params(years: Optional[Union[int, List[int]]],
               states: Optional[Union[str, List[str]]],
               actions: Optional[Union[Action, List[Action]]],
               races: Optional[Union[Race, List[Race]]]) -> Dict[str, str]:
    '''
    Creates parameter dictionary used in requests to HDMA API.

    Args:
        All args from parent function (get_params) are passed into corresponding "translate"
        functions, which correct for user error and ensure parameters will be valid.

    Returns:
        Dictionary
    '''
    params = {}

    if years:
        params['years'] = translate_years(years)
    if states:
        params['states'] = translate_states(states)
    if actions:
        params['actions_taken'] = translate_actions(actions)
    if races:
        params['races'] = translate_races(races)

    return params

### (Helper functions for API parameter function) Translate user input to valid string ###

def translate_years(years: Union[int, List[int]]) -> str:
    '''
    Checks user input and translates close matches into acceptable string format for API requests.

    Args:
        years(int | List[int]): a single 4-digit year or list of 4-digit years.

    Returns:
        String
    '''
    if isinstance(years, int):
        return str(years)
    return ','.join([str(year) for year in years])

def translate_states(states: Union[str, List[str]]) -> str:
    '''
    Checks user input and translates close matches into acceptable string format for API requests.

    Args:
        states(str | List[str]): input(s) to be checked against the 'state_set' variable (a set 
            containing all valid state arguments).

    Returns:
        String
    '''
    if type(states) == str:
        check_abbreviation(states)
        return states.replace(' ', '')
    elif isinstance(states, Iterable):
        states = list(states)
        check_abbreviation(states)
        return ','.join(states)
    else:
        raise TypeError(f"The input '{states}' is not a valid input.")

def translate_actions(actions: Union[Action, List[Action]]) -> str:
    '''
    Transform user input (selection from enum class) into acceptable string format for API requests.

    Args:
        actions(Action | List[Action]): Enum or list of enums from 'Action' enum class.

    Returns:
        String
    
    Raises:
        TypeError: If input is not of type 'Action' or 'List'.
    '''
    if type(actions) == Action:
        return convert_single_act(actions)
    elif type(actions) == list:
        return convert_multiple_acts(actions)
    else:
        raise TypeError(f"The input '{actions}' is not a valid input. Please input an option from the"
                        " 'Action' class or a List containing options from the 'Action' class.")

def translate_races(races: Union[Race, List[Race]]) -> str:
    '''
    Transform user input (selection from enum class) into acceptable string format for API requests.

    Args:
        races(Race | List[Race]): Enum or list of enums from 'Race' enum class.

    Returns:
        String
    
    Raises:
        TypeError: If input is not of type 'Race' or 'List'.
    '''
    if type(races) == Race:
        return convert_single_race(races)
    elif type(races) == list:
        return convert_multiple_races(races)
    else:
        raise TypeError(f"The input '{races}' is not a valid input. Please input an option from the"
                        " 'Race' class or a List containing options from the 'Race' class.")

### Other helper functions ###
def convert_single_act(action: Action) -> str:
    '''
    Converts a single 'Action' enum to a string if it is valid.

    Args:
        action(Action): A single enum from the 'Action' enum class.

    Returns:
        String

    Raises:
        ValueError: If input is not a valid 'Action' enum.
    '''
    if action not in Action:
        raise ValueError(f"The input '{action}' is not a valid action.")
    return str(action.value)

def convert_multiple_acts(actions: List[Action]) -> str:
    '''
    Converts multiple 'Action' enums to a string if they are valid.

    Args:
        actions(List[Action]): A list of enums from the 'Action' enum class.

    Returns:
        String
        
    Raises:
        ValueError: If input is not a valid 'Action' enum.
    '''
    act_text = []
    for i, act_input in enumerate(actions):
        if type(act_input) != Action or act_input not in Action:
            raise ValueError(f"The input '{act_input}' at index {i} is not a valid action.")
        else:
            act_text.append(str(act_input.value))
    return ','.join(act_text)

def convert_single_race(race: Race) -> str:
    '''
    Converts a single 'Race' enum to a string (via accessing 'race_dictionary', using the enum's 
    value as the dict key) if it is valid.

    Args:
        race(Race): A single enum from the 'Race' enum class.

    Returns:
        String
    
    Raises:
        ValueError: If input is not a valid 'Race' enum.
    '''
    if race not in Race:
        raise ValueError(f"The input '{race}' is not a valid race.")
    return race_dictionary[race.value]

def convert_multiple_races(races: List[Race]) -> str:
    '''
    Converts multiple 'Race' enums to a string (via accessing 'race_dictionary', using the enum's 
    value as the dict key) if they are valid.

    Args:
        races(List[Race]): A list of enums from the 'Race' enum class.

    Returns:
        String
    
    Raises:
        ValueError: If input is not a valid 'Race' enum.
    '''
    race_text = []
    for i, race_input in enumerate(races):
        if type(race_input) != Race or race_input not in Race:
            raise ValueError(f"The input '{race_input}' at index {i} is not a valid race.")
        else:
            race_text.append(race_dictionary[race_input.value])
    return ','.join(race_text)

def check_abbreviation(states: Union[str, List[str]]) -> None:
    '''
    Checks to make sure input is one of the Two-Letter State Abbreviations listed in 'state_set'.

    Args:
        states(str | List[str]): A single or list of single state abbreviation(s).

    Returns:
        None

    Raises:
        ValueError: If input is not found in 'state_set'.
    '''
    if type(states) == str:
        states = states.replace(' ', '')
        if states.upper() not in state_set:
            raise ValueError(
                f'The input \'{states}\' is not a valid state input. '\
                'Please ensure your input is a valid two-letter state abbreviation.\n'\
                'To pass multiple state inputs, please pass a List containing each individual '\
                'state to this function and try again.'
                )
    elif type(states) == list:
        for i, state_input in enumerate(states):
            state_input = state_input.replace(' ', '')
            if state_input.upper() not in state_set:
                raise ValueError(
                    f'The input \'{state_input}\' at index {i} of your list is not a valid input. '\
                    'Please ensure all inputs are valid two-letter state abbreviations.'
                    )
    return

### Testing functions ###

if __name__ == '__main__':

    # x1 = translate_races([Race.Asian,Race.Black,Race.Pacific_Islander])
    # print(x1, type(x1))

    # y1 = get_aggregations(2019, 'dc' , races=Race.UNAVAILABLE)
    # print(y1)
    # y2 = get_loans(2019, 'dc', [Action.INCOMPLETE, Action.PREAPPROVED], Race.PACIFIC_ISLANDER)
    # print(y2)
    # y3 = get_institutions(2020, ['dc', 'md', 'va'])
    # print(y3)

    f1a = translate_actions(Action.DENIED)
    f1b = translate_actions([Action.DENIED, Action.INCOMPLETE, Action.ORIGINATED])
    print(f1a, f1b, sep= ' | ')
    f2a = translate_races(Race.ASIAN)
    f2b = translate_races([Race.ASIAN, Race.BLACK, Race.JOINT])
    print(f2a,f2b, sep= ' | ') 
    f3a = translate_states(['dc', 'md', 'va']); print(f3a)
    # f3b = translate_states('dc,md,va'); print(f3b)
    f4 = translate_years(2018)
    print(f4)
