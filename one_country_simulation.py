"""Simulation file used to run the model"""
import time
from init_objects import *
from one_country_model import *

# 1 setup parameters
parameters = {
    # global parameters
    "n_domestic_assets": 1,
    "n_domestic_funds": 2,
    "domestic_inflation_mean": 0.0,
    "start_day": 1,
    "end_day": 101,
    "cov_memory": 0.00,
    # asset parameters
    "face_value": 5000,
    "nominal_interest_rate": 0.02/250,
    "currency_rate": 0.01/250,
    "maturity": 0.99936,
    "quantity": 5000,
    # agent parameters
    "price_memory": 0.0,
    "risk_aversion": 5.0,
    "news_evaluation_error": 0,
    # initial values
    "total_money": 1000,
    "init_agent_ewma_delta_prices": 1,
    "init_payouts": 0,
    "init_losses": 0,
    # shock processes parameters
    "domestic_default_events_mean": 80 / float(250),
    "domestic_default_events_std": 5 / float(250),
    "default_events_mean_reversion": 0.00,# 0.001,
    "domestic_default_rate_mean": 0.02 / float(80),
    "domestic_default_rate_std": 0,
    "default_rate_mean_reversion": 1,
    "adaptive_param": 0.0,
}

seed = 1

default_stats = {"mean_default_events": [15 / float(250), 15 / float(250), 75 / float(250), 75 / float(250)]}
default_stats.update({"default_events_std": [0.44 / float(250), 0.44 / float(250), 2.83 / float(250), 2.83 / float(250)]})
default_stats.update({"default_rate_mean": [0.005 / float(15), 0.02 / float(15), 0.005 / float(75), 0.02 / float(75)]})
default_stats.update({"default_rate_std": [0, 0, 0, 0]})
default_stats.update({"default_events_mean_reversion": [0.0011, 0.0011, 0.0014, 0.0014]})

# 2 initalise model objects
portfolios, currencies, funds, exogenous_agents = init_objects_one_country(parameters, default_stats, seed)

# 3 simulate model
start = time.time()
portfolios, currencies, exogenous_agents, funds = one_country_model(portfolios, currencies, parameters, exogenous_agents, funds, seed)
end = time.time()

print(end - start)
print("DONE!!!")
