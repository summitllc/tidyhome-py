"""Unit testing module for tidyhome.py.

Contains unique test cases for each main/helper function.
"""

import unittest # https://docs.python.org/3/library/unittest.html
import pandas as pd
from .. import tidyhome as th

### Main Function TestCases ###
class get_aggregations_TestCase(unittest.TestCase):
    """TestCase class for get_aggregations function in tidyhome.py"""

    def test_get_aggregations_no_actions_races(self):
        with self.assertRaises(Exception):
            th.get_aggregations(2018, "dc")

    def test_get_aggregations_returns_DataFrame(self):
        returndata = th.get_aggregations(
            2020,
            "DC" ,
            races=th.Race.UNAVAILABLE
        )
        self.assertIsInstance(returndata, pd.DataFrame)

class get_institutions_TestCase(unittest.TestCase):
    """TestCase class for get_institutions function in tidyhome.py"""

    def test_get_institutions_returns_DataFrame(self):
        returndata = th.get_institutions(
            2018,
            ["DC", "Md", "va"]
        )
        self.assertIsInstance(returndata, pd.DataFrame)

class get_loans_TestCase(unittest.TestCase):
    """TestCase class for get_loans function in tidyhome.py"""

    def test_get_loans_no_actions_races(self):
        with self.assertRaises(Exception):
            th.get_loans(2018, "dc")

    def test_get_loans_returns_DataFrame(self):
        returndata = th.get_loans(
            2019,
            "dc",
            [th.Action.INCOMPLETE, th.Action.PREAPPROVED],
            [th.Race.BLACK, th.Race.WHITE]
        )
        self.assertIsInstance(returndata, pd.DataFrame)


### Helper Function TestCases ###
class translate_years_TestCase(unittest.TestCase):
    """TestCase class for translate_years function in tidyhome.py"""

    def test_translate_years_int_to_str(self):
        self.assertEqual(th.translate_years(2020), "2020")

    def test_translate_years_list_to_str(self):
        self.assertEqual(th.translate_years([2020]), "2020")
        self.assertEqual(th.translate_years([2018, 2019, 2020]), "2018,2019,2020")
        self.assertEqual(th.translate_years((2020, 2021)), "2020,2021")

class translate_states_TestCase(unittest.TestCase):
    """TestCase class for translate_states function (and subsequent functions called by it) in 
    tidyhome.py"""

    def test_translate_states_removes_spaces(self):
        self.assertEqual(th.translate_states("dc"), "dc")
        self.assertEqual(th.translate_states("nY  "), "nY")
        self.assertEqual(th.translate_states(["ny ", "PA", "vA", " Fl"]), "ny,PA,vA,Fl")

    def test_check_abbreviation_invalid_inputs(self):
        with self.assertRaises(ValueError): th.check_abbreviation("Virginia")
        with self.assertRaises(ValueError): th.check_abbreviation("DC,MD,VA")
        with self.assertRaises(ValueError): th.check_abbreviation("XY")
        with self.assertRaises(ValueError): th.check_abbreviation(["DC","MD","VA","XY"])

class translate_actions_TestCase(unittest.TestCase):
    """TestCase class for translate_actions function (and subsequent functions called by it) in 
    tidyhome.py"""

    def test_translate_actions_invalid_input(self):
        with self.assertRaises(TypeError): 
            th.translate_actions("Originated")

    def test_translate_actions_single_enum_value_to_str(self):
        self.assertEqual(th.translate_actions_single(th.Action.PREAPPROVED), "8")

    def test_translate_actions_single_invalid_input(self):
        with self.assertRaises(TypeError): th.translate_actions_single("Originated")
        with self.assertRaises(TypeError): th.translate_actions_single(1)

    def test_translate_actions_multiple_enum_values_to_str(self):
        self.assertEqual(th.translate_actions_multiple([th.Action.PREAPPROVED, th.Action.ORIGINATED]), "8,1")

    def test_translate_actions_multiple_invalid_input(self):
        with self.assertRaises(TypeError): th.translate_actions_multiple([th.Action.APPROVED, "Withdrawn"])
        with self.assertRaises(TypeError): th.translate_actions_multiple([th.Action.DENIED, 2])

class translate_races_TestCase(unittest.TestCase):
    """TestCase class for translate_races function (and subsequent functions called by it) in 
    tidyhome.py"""

    def test_translate_races_invalid_input(self):
        with self.assertRaises(TypeError): 
            th.translate_races("Joint")

    def test_translate_races_single_enum_value_to_str(self):
        self.assertEqual(th.translate_races_single(th.Race.ASIAN), "Asian")

    def test_translate_races_single_invalid_input(self):
        with self.assertRaises(TypeError): th.translate_races_single("Asian")
        with self.assertRaises(TypeError): th.translate_races_single(0)

    def test_translate_races_multiple_enum_values_to_str(self):   
        self.assertEqual(th.translate_races_multiple([th.Race.BLACK, th.Race.WHITE]), "Black or African American,White")

    def test_translate_races_multiple_invalid_inputs(self):
        with self.assertRaises(TypeError): th.translate_races_multiple([th.Race.JOINT, "American Indian or Alaska Native"])
        with self.assertRaises(TypeError): th.translate_races_multiple([th.Race.UNAVAILABLE, 4])


if __name__ == '__main__':
    unittest.main()
