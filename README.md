# tidyhome: a package for accessing CFPB U.S. home mortgage data

[![PyPI Latest Release](https://img.shields.io/pypi/v/tidyhome)](https://pypi.org/project/tidyhome/)

## What is tidyhome?

Tidyhome is a package that simplifies the process of retrieving Home Mortgage Disclosure Act (HMDA) data from the Consumer Financial Protection Bureau's (CFPB) [HMDA Platform API](https://cfpb.github.io/hmda-platform/#hmda-api-documentation).

The 'HMDA Platform API' refers to several APIs designed to handle various tasks. Of these APIs, tidyhome interacts with the 'Data Browser' API.

The goal of tidyhome is to allow users the option to circumnavigate making API requests in their web browser. The freedom to do so may prove useful to data scientists who are tasked with analyzing HMDA data.

## Installation

Install tidyhome using:

```python
pip install tidyhome
```

## How to use tidyhome

Tidyhome contains several classes and functions that are designed to simplify and guide the process of making a valid API request.

Below is a brief overview of each class/function and an example of how tidyhome can be used.

### Classes:

* ```Race```: an enumerated class containing races recorded as part of a home mortgage application or loan. To be used as input to a function's 'races' parameter to get data for only the races you specify.

* ```Action```: an enumerated class containing actions taken by lending institutions on the filed application or loan. To be used as input to a function's 'actions' parameter to get data for only the actions you specify.

### Functions:

* ```get_aggregations```: returns a pandas DataFrame containing aggregate data of all loans reported.

* ```get_loans```: returns a pandas DataFrame containing all lending institutions that reported HMDA data.

* ```get_institutions```: returns a pandas DataFrame containing raw HMDA data on all individual loans reported.

*Click [here](https://github.com/pandas-dev/pandas) for more information regarding pandas, a powerful Python data analysis package.*

### Usage example:

```python
>>> import tidyhome as th
>>> th.get_loans(2019, "dc", th.Action.INCOMPLETE, [th.Race.BLACK, th.Race.WHITE])
```

The above function call returns a DataFrame containing HMDA data on all individual loans in 2019 in DC where the file was closed for incompleteness and the reported races of applicants/borrowers were black or white.

------------

Github Page: https://github.com/summitllc/tidyhome-py

Bug Tracking Page: https://github.com/summitllc/tidyhome-py/issues
