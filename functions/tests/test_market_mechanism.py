from numpy.testing import assert_equal
from functions.market_mechanism import *
import pytest

#
import pandas as pd
import numpy as np


#To create objects we will test with
from objects.currency import *
from objects.fund import *
from objects.asset import *


# Like in tests_expectation formation
def funds_and_assets(n_d, n_f,    ):
    
    portfolios = []
    asset_nationalities = ['domestic', 'foreign', 'domestic', 'foreign']
    
    for idx in range(n_d+n_f):     # pass in parameters and variables    #          country, #   face_value, nominal_interest_rate, maturity, quantity
        asset_params = AssetParameters(asset_nationalities[idx], 100, 0.002, 0.99, 500)  #  
        init_asset_vars = AssetVariables(1, 0.001)  #   price, default_rate 
        previous_assets_vars = AssetVariables(1, 0.0005)  # price, default_rate 
            
        portfolios.append(Asset(idx, init_asset_vars, previous_assets_vars, asset_params))
    

    print(portfolios)
 

def price_adjustment(portfolios, currencies, environment, exogeneous_agents , funds, asset_object):
    pass

    
funds_and_assets(2, 2 )

 

