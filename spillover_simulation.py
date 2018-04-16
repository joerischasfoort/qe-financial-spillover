"""Simulation file used to run the model"""
import pandas as pd

from init_objects import *
from spillover_model import *

# 1 setup parameters
parameters = { #Todo: cleaning and spell checking!!
    # global parameters
    "n_domestic_assets": 1,
    "n_foreign_assets": 1,
    "n_domestic_funds": 1,
    "n_foreign_funds": 1,
    "domestic_inflation_std": 0.01,
    "foreign_inflation_std": 0.02,
    "days": 100,
    "p_change_intensity": 0.1,
    "fx_change_intensity": 0.1,
    "cov_memory": 0.01,
    # asset parameters
    "face_value": 5000,
    "nominal_interest_rate": 0.04/250,
    "currency_rate": 0.03/250,
    "maturity" : 0.995,
    "quantity" : 5000,
    # agent parameters
    "price_memory": 0.0,
    "fx_memory": 0.0,
    "risk_aversion": 2.0,
    "news_evaluation_error": 0.05,
    # cb parameters
    "cb_country": 'domestic',
    # initial values
    "init_asset_price": 1.0,
    "init_exchange_rate": 1.0,
    "total_money": 4000,
    "init_agent_ewma_delta_prices": 1,
    "init_ewma_delta_fx": 1,
    "init_asset_demand": 0,
    "init_currency_demand": 0,
    "init_payouts": 0,
    "init_losses": 0,
    "init_profits": 0,
    # shock processes parameters
    "fx_shock_mu": 0.0,
    "fx_shock_std": 0.00001,
    "avg_yearly_default_events": 80,
    "avg_yearly_default_events_std":0,#0.05,
    "avg_yearly_default_events_mean_reversion": 1,# 0.001,
    "default_rate_mu": -7.6, #the mean and standard deviation are not the values for the distribution itself, but of the underlying normal distribution it is derived from.
    "default_rate_std": 0.4,
    "default_rate_mean_reversion": 1,
    "default_rate_delta_t": 0.003968253968253968,
    "adaptive_param": 0.1,
}

# 2 initalise model objects
portfolios, currencies, funds, environment, exogenous_agents = init_objects(parameters)
#print(portfolios, currencies, funds, environment, exogeneous_agents)

# 3 simulate model
portfolios, currencies, environment, exogenous_agents, funds, data_t = spillover_model(portfolios, currencies, environment, exogenous_agents, funds, seed=1)

