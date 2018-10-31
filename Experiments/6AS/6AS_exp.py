"""Simulation file used to run the model"""
import os

import sys
import time


sys.path.append('/home/jriedler/qe-financial-spillover')
from spillover_model import *
from init_objects_6a import *







list_of_risk_correlation = {}
list_of_risk_correlation.update({'domestic_inflation'+"_and_" +'foreign_inflation': 0.0})
list_of_risk_correlation.update({'foreign_inflation'+"_and_" +'domestic_inflation': list_of_risk_correlation['domestic_inflation'+"_and_" +'foreign_inflation']})
list_of_risk_correlation.update({'domestic_inflation'+"_and_" +'fx_shock': -0.0})
#list_of_risk_correlation.update({'foreign_inflation'+"_and_" +'domestic_fx_shock': -0.17})


# 1 setup parameters
parameters = { #Todo: cleaning and spell checking!!
    # global parameters
    "n_domestic_assets": 3,
    "n_foreign_assets": 3,
    "n_domestic_funds": 1,
    "n_foreign_funds": 1,
    "list_risk_corr": list_of_risk_correlation,
    "domestic_price_index": 1,
    "foreign_price_index": 1,
    "domestic_inflation_mean": 0.0,
    "foreign_inflation_mean": 0.0,
    "domestic_inflation_std": 0.02/float(250),
    "foreign_inflation_std": 0.02/float(250),
    "start_day": 1,
    "end_day": 5001,
    "p_change_intensity": 0.0001,
    "fx_change_intensity": 0.0001,
    "cov_memory": 0.00,
    # asset parameters
    "face_value": 5000,
    "nominal_interest_rate": 0.02/250,
    "currency_rate": 0.0/250,
    "maturity" : 0.9996,
    "quantity" : 5000,
    # agent parameters
    "price_memory": 0.0,
    "fx_memory": 0.0,
    "fx_reversion_speed": 0.15/250,
    "local_currency_return_weight": 1,
    "risk_aversion": 5.0,
    "domestic_risk_aversion_D_asset": 5,
    "domestic_risk_aversion_F_asset": 5,
    "foreign_risk_aversion_D_asset": 5,
    "foreign_risk_aversion_F_asset": 5,
    "news_evaluation_error": 0,
    # cb parameters
    "cb_country": 'domestic',
    # initial values
    "init_asset_price": 1.0,
    "init_exchange_rate": 1.0,
    "total_money": 2500,
    "init_agent_ewma_delta_prices": 1,
    "init_ewma_delta_fx": 1,
    "init_asset_demand": 0,
    "init_currency_demand": 0,
    "init_payouts": 0,
    "init_losses": 0,
    "init_profits": 0,
    # shock processes parameters
    "fx_shock_mean": 0.0,
    "fx_shock_std": 0.0,
    "domestic_default_events_mean": 80 / float(250),
    "foreign_default_events_mean": 80 / float(250),
    "domestic_default_events_std": 10 / float(250),
    "foreign_default_events_std": 10 / float(250),
    "default_events_mean_reversion": 1,# 0.001,
    "domestic_default_rate_mean": 0.02 / float(80),
    "foreign_default_rate_mean": 0.02 / float(80),
    "domestic_default_rate_std": 0,
    "foreign_default_rate_std": 0,
    "default_rate_mean_reversion": 1,
    "default_rate_delta_t": 0.003968253968253968,
    'conv_bound': 0.001,
    "adaptive_param": 0.0,
}



obj_label = "6a_lcb"
seed = 1

saving_params = {}
saving_params.update({"path": '/home/jriedler/qe-financial-spillover/Experiments/6AS/Objects_6AS/'})
saving_params.update({"time": 0})

maturities = [0.98,0.9996,1]*2
face_values=[2500,5000,5000]*2
quantities = face_values



# 2 initalise model objects
portfolios, currencies, funds, environment, exogenous_agents = init_objects_6a(parameters, maturities, face_values, quantities, seed)








# 3 simulate model
start = time.time()
portfolios, currencies, environment, exogenous_agents, funds, data_t = spillover_model(portfolios, currencies, environment, exogenous_agents, funds, seed, obj_label, saving_params)
end = time.time()
print(end - start)

print("DONE!!!")
print(pd.__version__)
