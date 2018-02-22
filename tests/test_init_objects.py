from init_objects import *
from objects.parameters import *
from numpy.testing import assert_equal
import pytest

@pytest.fixture
def global_parameters():
    """Returns global parameter which indicates there are four assets"""
    class GlobalParameter:
        def __init__(self, n_assets):
            self.n_assets = n_assets
    return GlobalParameter(4)

@pytest.fixture
def init_asset_vars():
    """Returns initial asset variable with price == 1"""
    return AssetInitialVariables(1)

@pytest.fixture
def asset_params():
    """Returns a class filled with initial asset variables"""
    return AssetParameters('domestic', 100, 0.12, 0.3, 0.003, 5000)


def test_init_objects(global_parameters, init_asset_vars, asset_params):
    funds, assets = init_objects(global_parameters, init_asset_vars, init_asset_vars, asset_params)
    # the function creates four assets
    assert_equal(len(assets), 4)


#test_init_objects(global_parameters(), init_asset_vars(), asset_params())