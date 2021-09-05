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
from check_dictionaries import state_dictionary, race_dictionary

# Limit what gets imported via the 'import *' statement
__all__ = [
    'get_aggregations',
    'get_institutions',
    'get_loans'
]

class Race(Enum):
    Asian = 0
    Pacific_Islander = 1
    Free_Form = 2
    Unavailable = 3
    Native_American = 4
    Black = 5
    Mixed_Minority = 6
    White = 7
    Joint = 8
    
# Values correspond with actions recognized by HDMA API
class Action(Enum):
    Originated = 1
    Approved = 2
    Denied = 3
    Withdrawn = 4
    Incomplete = 5
    Purchased = 6
    Predenied = 7
    Preapproved = 8

### (Main functions) ###

def get_aggregations(years: str, states: Union[List[str], str], actions: Union[List[Enum], Enum]= None, races: Union[List[Enum], Enum] = None) -> pd.DataFrame:
    '''
    Send request to HDMA API to get aggregations.
        
    Args:
        years (Str): year in the range 2018-2020. (Only one year should be passed for each call, since the HDMA API can only show data for one year per request.)\ 
            ['2018', '2019', '2020']

        states (List | Str): valid Two-Letter State Abbreviations for US state or territory.
            ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA',\ 
            'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',\ 
            'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', 'AS', 'GU', 'MP', 'PR', 'VI', 'UM', 'FM', 'MH', 'PW']

        actions (List | Enum): action(s) taken by population information is being requested for. A valid parameter should be selected from the following options:\ 
            [Action.Originated, Action.Approved, Action.Denied, Action.Withdrawn, Action.Incomplete, Action.Purchased,\ 
            Action.Predenied, Action.Preapproved]

        races (List | Enum): race(s) of population information is being requested for. A valid parameter should be selected from the following options:\ 
            [Race.Asian, Race.Pacific_Islander, Race.Free_Form, Race.Unavailable, Race.Native_American, Race.Black, Race.Mixed_Minority,\ 
            Race.White, Race.Joint]
    
    Returns:
        pandas.DataFrame

    Raises:
        Exception: If HTTP request to API contains bad syntax or cannot be fulfilled.
    '''
    if actions == None and races == None:
        raise Exception("This function requires at least three parameters to make a proper request. Please add one then try again.")
    else:
        param_dict= get_params(years, states, actions, races)

        print('pulling aggregations data .....')
        urlendpoint = "https://ffiec.cfpb.gov/v2/data-browser-api/view/aggregations"
        r2 = requests.get(urlendpoint, params=param_dict)
        status = r2.status_code
        if status == 200:
            pass
        else:
            raise Exception(r2.text)
        x = r2.json()
        datalist = x["aggregations"]
        aggregations_df = pd.DataFrame(datalist)
        print('Aggregation DataFrame successfully created!')
        return aggregations_df

def get_institutions(years: str, states: Union[List[str], str], actions: Union[List[Enum], Enum]= None, races: Union[List[Enum], Enum]= None) -> pd.DataFrame:
    '''
    Get HMDA data by filing institutions
        
    Args:
        years (Str): year in the range 2018-2020. (Only one year should be passed for each call, since the HDMA API can only show data for one year per request.)\ 
            ['2018', '2019', '2020']

        states (List | Str): valid Two-Letter State Abbreviations for US state or territory.
            ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA',\ 
            'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',\ 
            'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', 'AS', 'GU', 'MP', 'PR', 'VI', 'UM', 'FM', 'MH', 'PW']

        actions (List | Enum): action(s) taken by population information is being requested for. A valid parameter should be selected from the following options:\ 
            [Action.Originated, Action.Approved, Action.Denied, Action.Withdrawn, Action.Incomplete, Action.Purchased,\ 
            Action.Predenied, Action.Preapproved]

        races (List | Enum): race(s) of population information is being requested for. A valid parameter should be selected from the following options:\ 
            [Race.Asian, Race.Pacific_Islander, Race.Free_Form, Race.Unavailable, Race.Native_American, Race.Black, Race.Mixed_Minority,\ 
            Race.White, Race.Joint]
    
    Returns:
        pandas.DataFrame

    Raises:
        Exception: If HTTP request to API contains bad syntax or cannot be fulfilled.
    '''
    param_dict = get_params(years, states, actions, races)

    print('pulling data on filing institutions .....')
    urlendpoint = "https://ffiec.cfpb.gov/v2/data-browser-api/view/filers"
    r2 = requests.get(urlendpoint, params=param_dict)
    status = r2.status_code
    if status == 200:
        pass
    else:
        raise Exception(r2.text)
    x = r2.json()
    datalist = x["institutions"]
    filers_df = pd.DataFrame(datalist)
    print('Institution DataFrame successfully created!')
    return filers_df

def get_loans(years: int, 
              states: Union[List[str], str], 
              actions: Optional[Union[Action, List[Action]]] = None, 
              races: Optional[Union[Race, List[Race]]] = None) -> pd.DataFrame:
    '''
    Get HMDA individual loan level data.
        
    Args:
        years (int): year in the range 2018-2020. (Only one year should be 
            passed for each call, since the HDMA API can only show data for one 
            year per request.)

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
        All args from parent function are passed into corresponding "translate" 
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
        years: Ideally, one year as str or int will be passed.\ 
            Function is prepared to handle int, str, or list[int | str].\ 
            Non-str arguments are converted to str.
    
    Returns:
        String
    '''
    if isinstance(years, int):
        return str(years)
    return ','.join([str(year) for year in years])

def translate_states(states: Union[List[str], str]) -> str:
    '''
    Checks user input and translates close matches into acceptable string format for API requests.
    
    Args:
        states: str or list[str].\ 
            Arguments are checked against the 'state_dictionary' variable.
    
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
        raise ValueError(f"The input '{states}' is not a valid input. Please try again.")

def translate_actions(actions: Union[List[Enum], Enum]) -> str:
    '''
    Transform user input (selection from enum class) into acceptable string format for API requests.
    
    Args:
        actions: Enum from 'Action' enum class
    
    Returns:
        String
    '''
    if isinstance(actions, Iterable): 
        actions = list(actions)
        for i, action_input in enumerate(actions):
            try:
                if action_input in Action:
                    actions[i] = str(action_input.value)
            except TypeError:
                raise TypeError("The input '{}' at index {} is not a valid action. "\
                                "Please refer to this function's docstring and input a valid option.".format(action_input, i))                
        return ','.join(actions)
    else:
        try:
            if actions in Action:
                pass
            else:
                raise TypeError
        except TypeError:
            raise TypeError("The input '{}' is not a valid action. "\
                            "Please refer to this function's docstring and input a valid option.".format(actions))
        return str(actions.value)

def translate_races(races: Union[List[Enum], Enum]) -> str:
    '''
    Transform user input (selection from enum class) into acceptable string format for API requests.
    
    Args:
        actions: Enum from 'Race' enum class
    
    Returns:
        String
    '''
    if isinstance(races, Iterable) and type(races) != str: 
        races = list(races)
        for i, race_input in enumerate(races):
            try:
                if race_input in Race:
                    races[i] = race_dictionary[race_input.value]
            except TypeError:
                raise TypeError("The input '{}' at index {} is not a valid race. "\
                                "Please refer to this function's docstring and input a valid option.".format(race_input, i))                
        return ','.join(races)
    else:
        try:
            if races in Race:
                pass
            else:
                raise TypeError
        except TypeError:
            raise TypeError("The input '{}' is not a valid race. "\
                            "Please refer to this function's docstring and input a valid option.".format(races))
        return race_dictionary[races.value]

### Other helper functions ###

def conv_to_str(integers: Union[List[int], int]) -> str:
    '''
    Converts integer input into a string.

    Args:
        integers: input as integer or an Iterable containing an integer.
    
    Returns:
        A single string (separated by commas if multiple integers were converted).
    '''
    if type(integers) == int:
        return str(integers)
    elif isinstance(integers, Iterable) and type(integers) != str:
        integers = [str(num) for num in integers]
        return ','.join(integers)
    else:
        return

def check_abbreviation(states: Union[str, List[str]]) -> None:
    '''
    Checks to make sure input one of the Two-Letter State Abbreviations listed in\ 
    the 'state_dictionary' variable.
    
    Args:
        states: A string or list (containing strings) of state name(s).
    
    Returns:
        None

    Raises:
        ValueError: If input is not found in 'state_dictionary'
    '''
    if type(states) == str:
        states = states.replace(' ', '')
        if states.upper() in state_dictionary:
            return
        elif len(states) > 2 and ',' in states:
            start_index = 0
            end_index = states.find(',')
            #Check sub-strings (between commas) to see if they are in 'state_dictionary'
            while end_index != -1:
                if states[start_index:end_index].upper() in state_dictionary:
                    #Next sub-string
                    start_index = end_index + 1
                    end_index = states.find(',', end_index + 1)
                else:
                    raise ValueError(
                        'The input \'{}\' is not a valid state input. '\
                        'Please ensure all inputs are valid two-letter state abbreviations (which have been listed '
                        'in this function\'s docstring, for ease of access purposes).'.format(states[start_index:end_index])
                        )
            #Final check outside of loop, to avoid infinite loop
            if states[start_index:].upper() not in state_dictionary:
                    raise ValueError(
                        'The input \'{}\' is not a valid state input. '\
                        'Please ensure all inputs are valid two-letter state abbreviations (which have been listed '
                        'in this function\'s docstring, for ease of access purposes).'.format(states[start_index:])
                        )
            return
        elif len(states) > 2 and ',' not in states:
            raise ValueError(
                'The input \'{}\' is not a valid state input. '\
                'Please ensure all inputs are valid two-letter state abbreviations (which have been listed '
                'in this function\'s docstring, for ease of access purposes).'.format(states)
                )
        else:
            raise ValueError(
                'The input \'{}\' is not a valid state input. '\
                'Please ensure all inputs are valid two-letter state abbreviations (which have been listed '
                'in this function\'s docstring, for ease of access purposes).'.format(states)
                )
    elif type(states) == list:
        for i, state_input in enumerate(states):
            if type(state_input) == str:
                if state_input.upper() not in state_dictionary:
                        raise ValueError(
                            'The input \'{}\' at index {} of your list is not a valid input. '\
                            'Please ensure all inputs are valid two-letter state abbreviations (which have been listed '
                            'in this function\'s docstring, for ease of access purposes).'.format(state_input, i)
                            )
            else:
                raise ValueError("The input '{}' at index {} of your list is not a valid input. Please try again.".format(state_input, i))                
        return

### Testing functions ###

if __name__ == '__main__':

    x1 = translate_races([Race.Asian,Race.Black,Race.Pacific_Islander])
    print(x1, type(x1))


    y1 = get_aggregations([2019], 'tx,md',races=Race.Mixed_Minority)
    print(y1)
    y2 = get_loans(2019, 'tx', [Action.Incomplete, Action.Predenied], Race.Pacific_Islander)
    print(y2)
    y3 = get_institutions(2020, ['ma', 'nj', 'tx'])
    print(y3)

    # print(state_dictionary.keys())
    # test = Race.Black