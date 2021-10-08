"""A package that simplifies the process of retrieving HMDA data from the HMDA Platform API

Tidyhome provides access to data on US home mortgages from CFPB's Home Mortgage Disclosure Act (HMDA)
Platform API via several functions. These functions make the proper API request (given your desired
parameters) and store the requested data in a pandas DataFrame. Currently, you can make requests to 
access data on individual loans, summaries of loans, and lending institutions.

    Usage examples:

    >>> tidyhome.get_institutions(2018, ["DC", "Md", "va"])
    
        -returns a DataFrame containing data on lending institutions that filed HMDA data in 2018 in 
         DC, Maryland, and Virginia.

    >>> tidyhome.get_loans(2019, "dc", [tidyhome.Action.INCOMPLETE, tidyhome.Action.PREAPPROVED], [tidyhome.Race.BLACK, tidyhome.Race.WHITE])
        
        -returns a DataFrame containing HMDA data on all individual loans in 2019 in DC where the file 
         was closed for incompleteness or the loan was preapproved, and the reported races of 
         applicants/borrowers were black or white.

    >>> tidyhome.get_aggregations(2020, "DC" , races=tidyhome.Race.UNAVAILABLE)

        -returns a DataFrame containing HMDA data on the total quantity and sum of all loans reported 
         in 2020 in DC where the reported race of applicants/borrowers was unavailable.
"""

# Copied from .tidyhome so that when `help(tidyhome)` is called, information for items in __all__
# is displayed after the docstring (also copied from .tidyhome)
__all__ = [
    "Race",
    "Action",
    "get_aggregations",
    "get_institutions",
    "get_loans"
]

# Will only import items listed in __all__
from .tidyhome import *

