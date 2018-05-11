from numpy.testing import assert_equal
from functions.distribute import *

""" Helper functions to assign funds to countries """

def test_distribute_options_equally():
    """Test if the distribute options equally function works"""
    assert_equal(distribute_options_equally(2, list_options=["US", "EU"]), ["US", "EU"])
    assert_equal(distribute_options_equally(4, list_options=["US", "EU"]), ["US", "EU", "US", "EU"])
    assert_equal(distribute_options_equally(4, list_options=["US", "EU", "SA"]), ["US", "EU", "SA", "US"])


def test_weighted_choice():
    assert_equal(weighted_choice(choices=[("Germany", 100), ("SA", 0)]), "Germany")


def test_ordered_list_of_countries():
    """Test if the order lists of countries produces the right type of list"""
    assert_equal(ordered_list_of_countries(2, 1), ['domestic', 'domestic', 'foreign'])
    assert_equal(ordered_list_of_countries(1, 2), ['domestic', 'foreign', 'foreign'])
    assert_equal(ordered_list_of_countries(1, 0), ['domestic'])
    assert_equal(ordered_list_of_countries(0, 1), ['foreign'])

