"""tidyhome.py unit testing using the built-in 'unittest' module"""
import append_src_tidyhome # necessary to successfully import tidyhome (via appending /src/tidyhome to sys.path)

import unittest # https://docs.python.org/3/library/unittest.html
import pandas as pd
import tidyhome as th


#Info on TestCase class: https://docs.python.org/3/library/unittest.html#unittest.TestCase
class TestTidyhome(unittest.TestCase):
    """Testcase class for functions in tidyhome.py"""

    ### Main functions ###
    def test_get_aggregations(self):
        with self.assertRaises(Exception):
            th.get_aggregations(2018, "dc")

        returndata = th.get_aggregations(
            2020,
            "DC" ,
            races=th.Race.UNAVAILABLE
        )
        self.assertIsInstance(returndata, pd.DataFrame)

    def test_get_institutions(self):
        returndata = th.get_institutions(
            2018,
            ["DC", "Md", "va"]
        )
        self.assertIsInstance(returndata, pd.DataFrame)

    def test_get_loans(self):
        with self.assertRaises(Exception):
            th.get_loans(2018, "dc")

        returndata = th.get_loans(
            2019,
            "dc",
            [th.Action.INCOMPLETE, th.Action.PREAPPROVED],
            [th.Race.BLACK, th.Race.WHITE]
        )
        self.assertIsInstance(returndata, pd.DataFrame)

    ### Helper functions ###
    def test_translate_years(self):
        self.assertEqual(th.translate_years(2020), "2020")
        self.assertEqual(th.translate_years([2020]), "2020")
        self.assertEqual(th.translate_years([2018, 2019, 2020]), "2018,2019,2020")
        self.assertEqual(th.translate_years((2020, 2021)), "2020,2021")

    def test_translate_states(self):
        self.assertEqual(th.translate_states("nY  "), "nY")
        self.assertEqual(th.translate_states(["ny ", "PA", "vA", " Fl"]), "ny,PA,vA,Fl")

    def test_check_abbreviation(self):
        with self.assertRaises(ValueError): th.check_abbreviation("Virginia")
        with self.assertRaises(ValueError): th.check_abbreviation("DC,MD,VA")
        with self.assertRaises(ValueError): th.check_abbreviation("XY")

    def test_translate_actions_single(self):
        self.assertEqual(th.translate_actions_single(th.Action.PREAPPROVED), "8")

        with self.assertRaises(TypeError):
            th.translate_actions_single("Originated")
        with self.assertRaises(TypeError):
            th.translate_actions_single(1)
    
    def test_translate_actions_multiple(self):
        self.assertEqual(th.translate_actions_multiple([th.Action.PREAPPROVED, th.Action.ORIGINATED]), "8,1")

        with self.assertRaises(TypeError):
            th.translate_actions_multiple([th.Action.APPROVED, "Withdrawn"])
        with self.assertRaises(TypeError):
            th.translate_actions_multiple([th.Action.DENIED, 2])

    def test_translate_races_single(self):
        self.assertEqual(th.translate_races_single(th.Race.ASIAN), "Asian")

        with self.assertRaises(TypeError):
            th.translate_races_single("Asian")
        with self.assertRaises(TypeError):
            th.translate_races_single(0)

    def test_translate_races_multiple(self):   
        self.assertEqual(th.translate_races_multiple([th.Race.BLACK, th.Race.WHITE]), "Black or African American,White")

        with self.assertRaises(TypeError):
            th.translate_races_multiple([th.Race.JOINT, "American Indian or Alaska Native"])
        with self.assertRaises(TypeError):
            th.translate_races_multiple([th.Race.UNAVAILABLE, 4])


if __name__ == '__main__':
    unittest.main()
