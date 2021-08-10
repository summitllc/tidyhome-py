####################################
#AUTHOR: Conor Gill - Summit Consulting
#PURPOSE: To circumnavigate the HMDA API for entry-level data scientists
#INPUT: A list of variables that I want from the HMDA Data
#OUTPUT: a dataframe with the variables asked for by user
#NOTES:
#    https://cfpb.github.io/hmda-platform/#hmda-api-documentation
#    https://requests.readthedocs.io/en/master/
#    https://packaging.python.org/tutorials/packaging-projects/
####################################

# import necessary packages
import pandas as pd
import os
import json
import csv
import requests


__all__ = [
    'get_aggregations',
    'get_institutions',
    'get_loans',
    'TidyHome',
    'add_one'
]

def api_translate(acts, yrs, sts, rcs):
    '''
    this takes the user input parameters and turns them into a dictionary for the endpoint
    making sure to correct for any user error and intuitive language
    '''

    if acts != None:
        actionsDict = {
            "1" : "originated",
            "2" : "approved",
            "3" : "denied",
            "4" : "withdrawn",
            "5" : "incomplete",
            "6" : "purchased",
            "7" : "predenied",
            "8" : "preapproved"}

        realActions = ""
        for i in actionsDict:
            if actionsDict[i] in acts:
                realActions += (i+",")
        acts = realActions
        acts = acts.lower().replace(" ",'').strip(" ,")

    if rcs != None:
        # to be used if we wanted to make it easier to specify race
        raceDict = {
            "asian" :"asian",
            "native hawaiian or other pacific islander" : "hawaiian",
            "Free Form Text Only" : "other",
            "Race Not Available" :"na",
            "American Indian or Alaska Native" :"american indian",
            "Black or African American" :"black",
            "2 or more minority races" :"mixed minority",
            "White" :"white",
            "Joint" :"joint"
        }
        rcs = rcs.lower().replace(" ",'').strip(" ,")

    yrs = yrs.lower().replace(" ",'').strip(" ,")
    sts = sts.lower().replace(" ",'').strip(" ,")

    ourdict = {
        "actions_taken": acts,
        "years" : yrs,
        "states" : sts,
        "races": rcs}

    if ourdict['actions_taken'] == None:
        del ourdict['actions_taken']
    if ourdict['races'] == None:
        del ourdict['races']

    return ourdict

def get_aggregations(param_dict) -> pd.DataFrame:
    '''
    Get aggregations for HMDA
    '''

    print('pulling aggregations data .....')
    urlendpoint = "https://ffiec.cfpb.gov/v2/data-browser-api/view/aggregations?"
    r2 = requests.get(urlendpoint, params=param_dict)
    status = r2.status_code
    if status == 200:
        status_msg = "successful"
    else:
        status_msg = "unsuccessful"
        print("the status of your get request is:", status_msg)
        print("try again and remember that you must have actions, states, years, and race listed")
        exit()
    x = r2.json()
    datalist = x["aggregations"]
    aggregations_df = pd.DataFrame(datalist)
    return aggregations_df

def get_institutions(param_dict) -> pd.DataFrame:
    '''
    Get HMDA data by filing institutions
    '''

    print('pulling data on filing institutions .....')
    urlendpoint = "https://ffiec.cfpb.gov/v2/data-browser-api/view/filers?"
    r2 = requests.get(urlendpoint, params=param_dict)
    status = r2.status_code
    if status == 200:
        status_msg = "successful"
    else:
        status_msg = "unsuccessful"
        print("the status of your get request is:", status_msg)
        print("try again and remember that you must have actions, states, years, and race listed")
        exit()
    x = r2.json()
    datalist = x["institutions"]
    filers_df = pd.DataFrame(datalist)
    return filers_df

def get_loans() -> pd.DataFrame:
    '''
    Get HMDA individual loan level data
    '''

    print('pulling loan level data .....')
    urlendpoint = "https://ffiec.cfpb.gov/v2/data-browser-api/view/csv?"
    r2 = requests.get(urlendpoint, params=param_dict)
    url = r2.url
    status = r2.status_code
    if status == 200:
        status_msg = "successful"
    else:
        status_msg = "unsuccessful"
        print("the status of your get request is:", status_msg)
        print("try again and remember that you must have actions, states, years, and race listed")
        exit()
    loans_df = pd.read_csv(url, low_memory=False)
    return loans_df

def add_one(number):
    return number + 1

def TidyHome(type, years, states, actions=None, races=None):
    if type == "aggregations":
        final_pmeters = api_translate(acts=actions, yrs=years, sts=states, rcs=races)
        daddyDF = get_aggregations(final_pmeters)
    elif type == "loans":
        final_pmeters = api_translate(acts=actions, yrs=years, sts=states, rcs=races)
        daddyDF = get_loans(final_pmeters)
    elif type == "filers":
        final_pmeters = api_translate(acts=actions, yrs=years, sts=states, rcs=races)
        daddyDF = get_institutions(final_pmeters)
    else:
        print('please enter a valid type! The options are: aggregations, loans, or filers')
        exit()
    print('successful download!')
    return daddyDF
