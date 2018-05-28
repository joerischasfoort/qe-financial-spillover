

from spillover_model import *
from multiprocessing import Process
from init_objects import *






list_of_risk_correlation = {}
list_of_risk_correlation.update({'domestic_inflation'+"_and_" +'foreign_inflation': 0.3})
list_of_risk_correlation.update({'foreign_inflation'+"_and_" +'domestic_inflation': list_of_risk_correlation['domestic_inflation'+"_and_" +'foreign_inflation']})
list_of_risk_correlation.update({'domestic_inflation'+"_and_" +'fx_shock': -0.3})
#list_of_risk_correlation.update({'foreign_inflation'+"_and_" +'domestic_fx_shock': -0.17})

# 1 setup parameters
parameters = { #Todo: cleaning and spell checking!!
    # global parameters
    "n_domestic_assets": 1,
    "n_foreign_assets": 1,
    "n_domestic_funds": 1,
    "n_foreign_funds": 1,
    "list_risk_corr": list_of_risk_correlation,
    "domestic_inflation_mean": 0.0,
    "foreign_inflation_mean": 0.0,
    "domestic_inflation_std": 0.01,
    "foreign_inflation_std": 0.02,
    "start_day": 1,
    "end_day": 3,
    "p_change_intensity": 0.1,
    "fx_change_intensity": 0.1,
    "cov_memory": 0.001,
    # asset parameters
    "face_value": 5000,
    "nominal_interest_rate": 0.04/250,
    "currency_rate": 0.03/250,
    "maturity" : 0.995,
    "quantity" : 5000,
    # agent parameters
    "price_memory": 0.0,
    "fx_memory": 0.0,
    "fx_reversion_speed": 0.01/250,
    "risk_aversion": 2.0,
    "news_evaluation_error": 0.00,
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
    "fx_shock_mean": 0.0,
    "fx_shock_std": 0.000001,
    "domestic_default_events_mean": 80 / float(250),
    "foreign_default_events_mean": 160 / float(250),
    "domestic_default_events_std": 40 / float(250),
    "foreign_default_events_std": 80 / float(250),
    "default_events_mean_reversion": 1,# 0.001,
    "domestic_default_rate_mean": 0.02 / float(80),
    "foreign_default_rate_mean": 0.02 / float(80),
    "domestic_default_rate_std": 0,
    "foreign_default_rate_std": 0,
    "default_rate_mean_reversion": 1,
    "default_rate_delta_t": 0.003968253968253968,
    "adaptive_param": 0.0,
}


seed = 1
if __name__ == '__main__':
    elasticities = [0.45,0.5]

    procs = []

    for index, number in enumerate(elasticities):

        parameters["fx_reversion_speed"]  = number/250
        obj_label = "fx_rev_speed_" + str(number)
        # 2 initalise model objects
        portfolios, currencies, funds, environment, exogenous_agents = init_objects(parameters)
        # print(portfolios, currencies, funds, environment, exogeneous_agents)

        proc = Process(target=spillover_model, args=(portfolios, currencies, environment, exogenous_agents, funds,  seed, obj_label))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()
