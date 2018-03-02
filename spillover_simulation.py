"""Simulation file used to run the model"""

from init_objects import *

# 1 setup parameters
parameters = {
    # global parameters
    "n_domestic assets": 2,
    "n_foreign_assets": 3,
    "n_domestic_funds": 3,
    "n_foreign_funds": 2,
    "days": 10,
    "p_change_intensity": 0.1,
    # asset parameters
    "face_value": 100,
    "default_rate" : 0.012,
    "nominal_interest_rate" : 0.003,
    "cash_return": 0,
    "maturity" : 1,
    "quantity" : 5000,
    # agent parameters
    "price_memory" : 2,
    "fx_memory" : 2,
    "risk_aversion" : 1,
    # initial values
    "init_asset_price" : 1,
    "init_exchange_rate" : 1,
    "total_money": 4000,
    "init_agent_ewma_delta_prices": 0,
    "init_ewma_delta_fx": 0
}

# 2 initalise model objects
assets, funds = init_objects(parameters)

# 3 simulate model
# assets, funds = spillover_model(assets, funds, parameters.days, parameters.gamma)

