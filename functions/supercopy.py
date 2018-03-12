from objects.fund import *


def copy_agent_variables(fund_var_object):
    """
    Takes an agent variable object and returns a copy with dictionary keys intact
    :param fund_object: object that will be copied
    :return: copied object
    """
    variables = vars(fund_var_object)
    new_variables = {}
    for variable in variables:
        if type(variables[variable]) == dict:
            new_variables[variable] = copy_dict(variables[variable])
        elif type(variables[variable]) == int or type(variables[variable]) == float:
            new_variables[variable] = variables[variable]
        else:
            new_variables[variable] = variables[variable].copy()

    obj = AgentVariables(assets=new_variables['assets'], currency=new_variables['currency'],
                         redeemable_shares=new_variables['redeemable_shares'], asset_demand=new_variables['asset_demand'],
                         currency_demand=new_variables['currency_demand'], ewma_returns=new_variables['ewma_returns'],
                         ewma_delta_prices=new_variables['ewma_delta_prices'],
                         ewma_delta_fx=new_variables['ewma_delta_fx'],
                         covariance_matrix=new_variables['covariance_matrix'],
                         payouts=new_variables['payouts'], weights=new_variables['weights'],
                         hypothetical_returns=new_variables['hypothetical_returns'])
    return obj


def copy_dict(dictionary):
    """
    Return a copy of a dictionary
    :param dictionary: input dictionary
    :return: dictionary copy
    """
    return {key: value for key, value in dictionary.items()}


