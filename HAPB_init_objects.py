from functions.initialize_assets import *
from functions.initialize_environment import *
from functions.initialize_agents import *


def init_objects(parameters, seed):
    """
    Function to initialise the model objects: first assets, then funds
    :param parameters: object which holds all model parameters
    :return: list of fund objects, list of asset objects
    """
    # 1 initialize portfolios
    portfolios = init_portfolios(parameters)

    # 2 initialize currencies
    currencies = init_currencies(parameters)

    # 3 initialize environment
    environment = init_environment(currencies, parameters)

    # 4 initialize funds
    funds = init_funds(environment,portfolios, currencies, parameters, seed)

    # 5 initialize exogenous agents
    exogenous_agents = init_exogenous_agents(portfolios, currencies, parameters)

    return portfolios, currencies, funds, environment, exogenous_agents