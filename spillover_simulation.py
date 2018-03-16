"""Simulation file used to run the model"""
import pandas as pd

from init_objects import *
from spillover_model import *

# 1 setup parameters
parameters = {
    # global parameters
    "n_domestic_assets": 1,
    "n_foreign_assets": 1,
    "n_domestic_funds": 1,
    "n_foreign_funds": 1,
    "days": 2,
    "p_change_intensity": 0.1,
    "fx_change_intensity": 0.1,
    # asset parameters
    "face_value": 5000,
    "nominal_interest_rate": 0.003,
    "currency_rate": 0,
    "maturity" : 0.99,
    "quantity" : 5000,
    # agent parameters
    "price_memory": 0.0,
    "fx_memory": 0.0,
    "risk_aversion": 1,
    "news_evaluation_error": 0.0001,
    # cb parameters
    "cb_country": 'domestic',
    # initial values
    "init_asset_price": 1,
    "init_exchange_rate": 1,
    "total_money": 4000,
    "init_agent_ewma_delta_prices": 1,
    "init_ewma_delta_fx": 1,
    "init_asset_demand": 0,
    "init_currency_demand": 0,
    "init_payouts": 0,
    "init_profits": 0,
    # shock processes parameters
    "fx_shock_mu": 0.0,
    "fx_shock_std": 0.001,
    "default_rate_mu": 0.00004,
    "default_rate_std": 0.00004,
    "default_rate_mean_reversion": 0.99,
    "default_rate_delta_t": 0.003968253968253968,
    "adaptive_param": 0.5
}

# 2 initalise model objects
portfolios, currencies, funds, environment, exogeneous_agents = init_objects(parameters)
#print(portfolios, currencies, funds, environment, exogeneous_agents)

# 3 simulate model
spillover_model(portfolios, currencies, environment, exogeneous_agents, funds,  seed=1)

