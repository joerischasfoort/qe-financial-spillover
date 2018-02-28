"""Simulation file used to run the model"""

from init_objects import *
from objects.modelparameters import *

# 1 setup parameters

parameters = ModelParameters(n_assets=4, 
                             n_funds=2, 
                             days=10, regions=['domestic', 'foreign'],
                             price_memory=2, fx_memory=2, risk_aversion=1, total_money=4000,
                             face_value=100, default_rate=0.12,
                             nominal_interest_rate=0.003, maturity=1,
                             quantity=5000, init_asset_price=1, init_exchange_rate=1, cash_return=0,
                             p_change_intensity=0.1)

# 2 initalise model objects
assets, funds = init_objects(parameters)

        
# 3 simulate model
# assets, funds = spillover_model(assets, funds, parameters.days, parameters.gamma)

