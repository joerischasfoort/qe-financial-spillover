from functions.initialize_assets import *
from functions.initialize_environment import *
from functions.initialize_agents import *


def init_objects_4a(parameters,maturities_4a, face_values_4a, quantities_4a, coupon_rates_4a, currency_rates_4a, currency_amounts_4a, p_holdings_4a, c_holdings_4a, risk_aversions_4a, default_stats, seed):
    """
    Function to initialise the model objects: first assets, then funds
    :param parameters: object which holds all model parameters
    :return: list of fund objects, list of asset objects
    """
    # 1 initialize portfolios
    portfolios = init_portfolios_4a(parameters,maturities_4a, face_values_4a, quantities_4a, coupon_rates_4a, default_stats)

    # 2 initialize currencies
    currencies = init_currencies_4a(parameters, currency_rates_4a, currency_amounts_4a)

    # 3 initialize environment
    environment = init_environment(currencies, parameters)

    # 4 initialize funds
    funds = init_funds_4a(environment,portfolios, p_holdings_4a, currencies, c_holdings_4a, parameters, risk_aversions_4a, seed)

    # 5 initialize exogenous agents
    exogenous_agents = init_exogenous_agents(portfolios, currencies, parameters)

    return portfolios, currencies, funds, environment, exogenous_agents



