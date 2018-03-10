from numpy.testing import assert_equal
from functions.supercopy import *
import pytest
import pandas as pd


@pytest.fixture
def fund_variables():
    class Obj:
        def __init__(self, name):
            self.name = name

        def __repr__(self):
            return 'Kewl' + str(self.name)

    obj1 = Obj('asset0')
    obj2 = Obj('asset1')

    variables = AgentVariables(assets={obj1: 20, obj2: 30}, currency={'currency1': 20},
                               redeemable_shares=10, asset_demand={obj1: 1, obj2: 2},
                               currency_demand={'currency1': 2}, ewma_returns={obj1: 2, obj2: 3},
                               ewma_delta_prices={obj1: 2, obj2: 3},
                               ewma_delta_fx={'currency1': 2},
                               covariance_matrix=pd.DataFrame({obj1: [1, 2], obj2: [0, 2]}),
                               payouts={obj1: 2, obj2: 2}, weights={obj1: 2, obj2: 3},
                               realised_returns={obj1: 0, obj2:0})
    return variables, obj1, obj2


@pytest.fixture
def dict_with_classes():
    class Obj:
        def __init__(self, name):
            self.name = name

    obj1 = Obj('I')
    obj2 = Obj('You')
    dict_class = {obj1: 2, obj2: 3}
    return dict_class


def test_copy_normal_dict():
    """check if a copied dictionary values are seperate"""
    some_dict = {'asset1': 2, 'asset3': 4}
    copy_some_dict = copy_dict(some_dict)
    assert_equal(copy_some_dict, some_dict)
    some_dict['asset1'] = 3
    assert_equal(some_dict == copy_some_dict, False)


def test_copy_obj_dict(dict_with_classes):
    """check if a copied dictionary keys are not copied if they are an object"""
    some_dict = dict_with_classes
    copy_some_dict = copy_dict(some_dict)
    assert_equal(copy_some_dict, some_dict)
    assert_equal(copy_some_dict == some_dict, True)


def test_copy_agent_variables(fund_variables):
    """check if a super copy of fund variables can still be accessed through the object while values do change"""
    variables, obj1, obj2 = fund_variables
    previous_variables = copy_agent_variables(variables)
    assert_equal(previous_variables.assets[obj1], variables.assets[obj1])
    variables.assets[obj1] = 1
    assert_equal(previous_variables.assets[obj1] == variables.assets[obj1], False)
