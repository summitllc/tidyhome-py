"""a package that simplifies the process of retrieving HMDA data from the HMDA Platform API

Tidyhome provides access to data on US home mortgages from CFPB's Home Mortgage Disclosure Act (HMDA)
Platform API via several functions. These functions make the proper API request (given your desired
parameters) and store the requested data in a pandas DataFrame. Currently, you can make requests to 
access data on individual loans, summaries of loans, and lending institutions.

    Usage examples:

    tidyhome.get_institutions(2018, ["DC", "Md", "va"])
        -returns a DataFrame containing data on lending institutions that filed HMDA data in 2018 in 
         DC, Maryland, and Virginia.
    tidyhome.get_loans(2019, "dc", [Action.INCOMPLETE, Action.PREAPPROVED], [Race.BLACK, Race.WHITE])
        -returns a DataFrame containing HMDA data on all individual loans in 2019 in DC where the file 
         was closed for incompleteness or the loan was preapproved, and the reported races of 
         applicants/borrowers were black or white.
    tidyhome.get_aggregations(2020, "DC" , races=Race.UNAVAILABLE)
        -returns a DataFrame containing HMDA data on the total quantity and sum of all loans reported 
         in 2020 in DC where the reported race of applicants/borrowers was unavailable.
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
import lookup

# Limit what gets imported via the 'import *' statement
__all__ = [
    "Race",
    "Action",
    "get_aggregations",
    "get_institutions",
    "get_loans"
]

class Race(Enum):
    """Races recorded as part of a home mortgage application or loan. You can use these to get data
    for only the races you specify."""
    ASIAN = 0
    PACIFIC_ISLANDER = 1
    FREE_FORM = 2
    UNAVAILABLE = 3
    NATIVE_AMERICAN = 4
    BLACK = 5
    MIXED_MINORITY = 6
    WHITE = 7
    JOINT = 8

# Values correspond with their proper 'Action Codes', as specified by CFPB
class Action(Enum):
    """Actions taken by lending institutions on the filed application or loan. You can use these
    to get data for only the actions you specify."""
    ORIGINATED = 1
    APPROVED = 2
    DENIED = 3
    WITHDRAWN = 4
    INCOMPLETE = 5
    PURCHASED = 6
    PREDENIED = 7
    PREAPPROVED = 8

### (Main functions) ###

def get_aggregations(year: int,
                     states: Union[str, List[str]],
                     actions: Optional[Union[Action, List[Action]]] = None,
                     races: Optional[Union[Race, List[Race]]] = None) -> pd.DataFrame:
    """
    Get HMDA aggregate data (ie. total quantity and sum) of all loans reported.

    Args:
        year (int): 
            Year that the HMDA data was filed in. Must be a *single* year from 2018 onwards 
            (currently the API only shows data for one year per request).

        states (str | List[str]): 
            State that the HMDA data was filed in. Must be a valid Two-Letter State Abbreviation
            for a US state or territory.

        actions (Action | List[Action]):
            Action taken on the application or loan by the lending institution that filed the HMDA
            data.

        races (Race | List[Race]):
            Reported race of the applicant or borrower in filed HMDA data.

    Returns:
        pandas.DataFrame

    Raises:
        Exception: If HTTP request to API contains bad syntax or cannot be fulfilled.
    """
    if not actions and not races:
        raise Exception("You must provide an argument to at least one of 'actions' or 'races'.")

    endpoint = "https://ffiec.cfpb.gov/v2/data-browser-api/view/aggregations"
    params= get_params(year, states, actions, races)
    response = requests.get(endpoint, params=params)

    if response.status_code != 200:
        raise Exception(response.text)

    data = response.json()
    return pd.DataFrame(data["aggregations"])

def get_institutions(year: int,
                     states: Union[str, List[str]],
                     actions: Optional[Union[Action, List[Action]]] = None,
                     races: Optional[Union[Race, List[Race]]] = None) -> pd.DataFrame:
    """
    Get all lending institutions that reported HMDA data.

    Args:
        year (int): 
            Year that the HMDA data was filed in. Must be a *single* year from 2018 onwards 
            (currently the API only shows data for one year per request).

        states (str | List[str]): 
            State that the HMDA data was filed in. Must be a valid Two-Letter State Abbreviation
            for a US state or territory.

        actions (Action | List[Action]):
            Action taken on the application or loan by the lending institution that filed the HMDA
            data.

        races (Race | List[Race]):
            Reported race of the applicant or borrower in filed HMDA data.

    Returns:
        pandas.DataFrame

    Raises:
        Exception: If HTTP request to API contains bad syntax or cannot be fulfilled.
    """
    endpoint = "https://ffiec.cfpb.gov/v2/data-browser-api/view/filers"
    params = get_params(year, states, actions, races)
    response = requests.get(endpoint, params=params)

    if response.status_code != 200:
        raise Exception(response.text)

    data = response.json()
    return pd.DataFrame(data["institutions"])

def get_loans(year: int,
              states: Union[str, List[str]],
              actions: Optional[Union[Action, List[Action]]] = None,
              races: Optional[Union[Race, List[Race]]] = None) -> pd.DataFrame:
    """
    Get raw HMDA data on all individual loans reported.

    Args:
        year (int): 
            Year that the HMDA data was filed in. Must be a *single* year from 2018 onwards 
            (currently the API only shows data for one year per request).

        states (str | List[str]): 
            State that the HMDA data was filed in. Must be a valid Two-Letter State Abbreviation
            for a US state or territory.

        actions (Action | List[Action]):
            Action taken on the application or loan by the lending institution that filed the HMDA
            data.

        races (Race | List[Race]):
            Reported race of the applicant or borrower in filed HMDA data.

    Returns:
        pandas.DataFrame

    Raises:
        Exception: If HTTP request to API contains bad syntax or cannot be fulfilled.
    """
    if not actions and not races:
        raise Exception("You must provide an argument to at least one of 'actions' or 'races'.")

    endpoint = "https://ffiec.cfpb.gov/v2/data-browser-api/view/csv"
    params = get_params(year, states, actions, races)
    response = requests.get(endpoint, params=params)

    if response.status_code != 200:
        raise Exception(response.text)

    data = pd.read_csv(response.url, low_memory=False)
    return data

### (Helper function for Main functions) Create API parameter dictionary ###

def get_params(year: Optional[Union[int, List[int]]],
               states: Optional[Union[str, List[str]]],
               actions: Optional[Union[Action, List[Action]]],
               races: Optional[Union[Race, List[Race]]]) -> Dict[str, str]:
    """
    Creates parameter dictionary used in requests to HMDA API.

    Args:
        All args from parent function (get_params) are passed into corresponding "translate"
        functions, which correct for user error and ensure parameters will be valid.

    Returns:
        Dictionary
    """
    params = {}

    if year:
        params["years"] = translate_years(year)
    if states:
        params["states"] = translate_states(states)
    if actions:
        params["actions_taken"] = translate_actions(actions)
    if races:
        params["races"] = translate_races(races)

    return params

### Helper functions (for 'get_params' function) ###

def translate_years(years: Union[int, List[int]]) -> str:
    """
    Checks user input and translates close matches into acceptable string format for API requests.

    Args:
        years(int | List[int]): a single 4-digit year or list of 4-digit years.

    Returns:
        String
    """
    if isinstance(years, int):
        return str(years)
    return ','.join([str(year) for year in years])

def translate_states(states: Union[str, List[str]]) -> str:
    """
    Checks user input and translates close matches into acceptable string format for API requests.

    Args:
        states(str | List[str]): a state or list of states to be validated.

    Returns:
        String
    """
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
    """
    Transforms user input (selection from enum class) into acceptable string format for API requests.

    Args:
        actions(Action | List[Action]): Enum or list of enums from 'Action' enum class.

    Returns:
        String
    
    Raises:
        TypeError: If input is not of type 'Action' or 'List'.
    """
    if type(actions) == Action:
        return translate_actions_single(actions)
    elif type(actions) == list:
        return translate_actions_multiple(actions)
    else:
        raise TypeError(f"The input '{actions}' is not a valid input. Please input an option from the"
                        " 'Action' class or a List containing options from the 'Action' class.")

def translate_races(races: Union[Race, List[Race]]) -> str:
    """
    Transform user input (selection from enum class) into acceptable string format for API requests.

    Args:
        races(Race | List[Race]): Enum or list of enums from 'Race' enum class.

    Returns:
        String
    
    Raises:
        TypeError: If input is not of type 'Race' or 'List'.
    """
    if type(races) == Race:
        return translate_races_single(races)
    elif type(races) == list:
        return translate_races_multiple(races)
    else:
        raise TypeError(f"The input '{races}' is not a valid input. Please input an option from the"
                        " 'Race' class or a List containing options from the 'Race' class.")

### Other helper functions ###

def translate_actions_single(action: Action) -> str:
    """
    Converts a single 'Action' enum to a string if it is valid.

    Args:
        action(Action): A single enum from the 'Action' enum class.

    Returns:
        String

    Raises:
        TypeError: If input is not an Action.
    """
    if not isinstance(action, Action):
        raise TypeError(f"'{action}' is not an Action.")
    return str(action.value)

def translate_actions_multiple(actions: List[Action]) -> str:
    """
    Converts multiple 'Action' enums to a string if they are valid.

    Args:
        actions(List[Action]): A list of enums from the 'Action' enum class.

    Returns:
        String
        
    Raises:
        TypeError: If input is not an Action.
    """
    act_text = []
    for action in actions:
        if not isinstance(action, Action):
            raise TypeError(f"'{action}' is not an Action.")
        else:
            act_text.append(str(action.value))
    return ','.join(act_text)

def translate_races_single(race: Race) -> str:
    """
    Converts a single 'Race' enum to a string (via accessing 'lookup.races', using the enum's 
    value as the dict key) if it is valid.

    Args:
        race(Race): A single enum from the 'Race' enum class.

    Returns:
        String
    
    Raises:
        TypeError: If input is not a Race.
    """
    if not isinstance(race, Race):
        raise TypeError(f"'{race}' is not a Race.")
    return lookup.races[race.value]

def translate_races_multiple(races: List[Race]) -> str:
    """
    Converts multiple 'Race' enums to a string (via accessing 'lookup.races', using the enum's 
    value as the dict key) if they are valid.

    Args:
        races(List[Race]): A list of enums from the 'Race' enum class.

    Returns:
        String
    
    Raises:
        TypeError: If input is not a Race.
    """
    race_text = []
    for race in races:
        if not isinstance(race, Race):
            raise TypeError(f"'{race}' is not a Race.")
        else:
            race_text.append(lookup.races[race.value])
    return ','.join(race_text)

def check_abbreviation(states: Union[str, List[str]]) -> None:
    """
    Checks to make sure input is one of the Two-Letter State Abbreviations listed in 'lookup.states'.

    Args:
        states(str | List[str]): A single or list of single state abbreviation(s).

    Returns:
        None

    Raises:
        ValueError: If input is not found in 'lookup.states'.
    """
    if type(states) == str:
        states = states.replace(' ', '')
        if states.upper() not in lookup.states:
            raise ValueError(
                f"The input '{states}' is not a valid state input. "\
                "Please ensure your input is a valid two-letter state abbreviation."\
                )
    elif type(states) == list:
        for state in states:
            state = state.replace(' ', '')
            if state.upper() not in lookup.states:
                raise ValueError(
                    f"'{state}' is not a valid input. "\
                    "Please ensure all inputs are valid two-letter state abbreviations."
                    )
    return
