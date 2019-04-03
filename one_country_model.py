import copy
import random
from functions.port_opt import *
from functions.asset_demands import *
from functions.ex_agent_asset_demands import *
from functions.balance_sheet_adjustments import *
from functions.stochasticprocess import *
from functions.expectation_formation import *
from functions.market_mechanism import *
from functions.profits_and_payouts import *
from functions.supercopy import *
from functions.measurement import *

from num_opt_pricing import *
import numpy as np
from scipy.optimize import minimize


def one_country_model(portfolios, currencies, environment, exogeneous_agents, funds, seed):
    """
    Koziol, Riedler & Schasfoort Agent-based simulation model of financial spillovers
    :param portfolios: list of asset portfolio objects
    :param currencies: list which contains the currency (single currency in this model)
    :param environment: Object which contains all the parameters
    :param exogeneous_agents: list which contains the central bank and underwriter agents
    :param funds: list of Fund objects
    :param days: integer amount of days over which the simulation will take place
    :param seed: integer used to seed the random number generator
    :return: lists of assets, funds
    """
    random.seed(seed)
    np.random.seed(seed)

    ##################################################################################
    ###################### COMPUTING STOCHASTIC PROCESSES ############################
    ##################################################################################
    # calculating stochastic components default
    days = environment.par.global_parameters["end_day"]
    if environment.par.global_parameters["start_day"] == 1:
        default_rates, fundamental_default_rate_expectation, shock_processes = stochastic_timeseries(
            environment.par.global_parameters, portfolios, days, seed)
    else:
        default_rates, fundamental_default_rate_expectation, shock_processes = stochastic_timeseries_2(
            environment.par.global_parameters, portfolios, environment.par.global_parameters['start_day'],
            environment.par.global_parameters['end_day'], seed)

    # initial default expectations TODO move this to initialization?
    noise = {}
    idiosyncratic_default_rate_noise = {}
    for j, fund in enumerate(funds):
        for i, a in enumerate(portfolios):
            random.seed(seed + j + i)
            np.random.seed(seed + j + i)
            noise[a] = [np.random.normal(0, fund.par.news_evaluation_error) for idx in range(days)]
            fund.exp.default_rates[a] = fundamental_default_rate_expectation[a][
                environment.par.global_parameters['start_day'] - 1]
        idiosyncratic_default_rate_noise[fund] = noise
    ####################################################################################
    ####################################################################################
    # creating individual intensity parameters
    for a in portfolios: #TODO: this should be taken care of in the initialization
        try:
            a.par.change_intensity
        except AttributeError:
            a.par.change_intensity = environment.par.global_parameters['p_change_intensity']

    # these two variables are needed for the pricing algorithm

    # var_t1 = []
    var_original = [v for v in var]
    var_t1 = [v for v in var]
    if "FX" in var:
        del var[var.index("FX")]


    ##############################################################################################################
    ############################################### DAY LOOP #####################################################
    ##############################################################################################################