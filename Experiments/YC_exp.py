import os

import sys


sys.path.append('/home/jriedler/qe-financial-spillover')
from spillover_model import *
from init_objects import *

seed = 1

variable = [0.952,0.984, 0.996, 0.9987,0.9992,0.9996,0.999733,0.9998,0.999867,0.9999,1]

list_of_risk_correlation = {}
list_of_risk_correlation.update({'domestic_inflation'+"_and_" +'foreign_inflation': 0.0})
list_of_risk_correlation.update({'foreign_inflation'+"_and_" +'domestic_inflation': list_of_risk_correlation['domestic_inflation'+"_and_" +'foreign_inflation']})
list_of_risk_correlation.update({'domestic_inflation'+"_and_" +'fx_shock': -0.0})
#list_of_risk_correlation.update({'foreign_inflation'+"_and_" +'domestic_fx_shock': -0.17})




# 1 setup parameters
parameters = { #Todo: cleaning and spell checking!!
    # global parameters
    "n_domestic_assets": 11,
    "n_foreign_assets": 11,
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
    "p_change_intensity": 0.1,
    "fx_change_intensity": 0.1,
    "cov_memory": 0.00,
    # asset parameters
    "face_value": 500,
    "nominal_interest_rate": 0.02/250,
    "currency_rate": 0.0/250,
    "maturity" : 0.9996,
    "quantity" : 500,
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
    "total_money": 1000,
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

    "adaptive_param": 0.0,
}






obj_label = "YC_all"

saving_params = {}
saving_params.update({"path": '/home/jriedler/qe-financial-spillover/Experiments/Yield_Curve/Objects_YC/'})
saving_params.update({"time": 0})




portfolios, currencies, funds, environment, exogenous_agents = init_objects(parameters, seed)

i=0
for a in portfolios:
    a.par.maturity = variable[i]
    i = i +1
    if i == len(variable)-1:
        i = 0
 



spillover_model(portfolios, currencies, environment, exogenous_agents, funds,  seed, obj_label,saving_params)





