from functions.initialize_assets import *
from functions.initialize_environment import *
from functions.initialize_agents import *



def init_objects_marketsize(parameters, seed, pos):
    """
    Function to initialise the model objects: first assets, then funds
    :param parameters: object which holds all model parameters
    :return: list of fund objects, list of asset objects
    """
    # 1 initialize portfolios
    portfolios = init_portfolios(parameters)


    # 2 initialize currencies
    currencies = init_currencies(parameters)

    for a in portfolios:
        if a.par.country == "domestic":
            new_quantity = ((a.par.quantity) * pos) / parameters["n_domestic_assets"]
            a.par.quantity = new_quantity
            a.par.face_value = new_quantity
            for c in currencies:
                if c.par.country == 'domestic':
                    new_quantity = ((a.par.quantity) * 0.1)
                    c.par.quantity = new_quantity
                    parameters["total_money"] = new_quantity

        if a.par.country == "foreign":
            new_quantity = ((a.par.quantity) ) / parameters["n_foreign_assets"]
            a.par.quantity = new_quantity
            a.par.face_value = new_quantity
            for c in currencies:
                if c.par.country == 'foreign':
                    new_quantity = ((a.par.quantity) * 0.1)
                    c.par.quantity = new_quantity
                    parameters["total_money"] += new_quantity
    # 3 initialize environment
    environment = init_environment(currencies, parameters)

    # 4 initialize funds
    funds = init_funds_marketsize(environment,portfolios, currencies, parameters, seed, pos)

    # 5 initialize exogenous agents
    exogeneous_agents = init_exogenous_agents(portfolios, currencies, parameters)


    return portfolios, currencies, funds, environment, exogeneous_agents



