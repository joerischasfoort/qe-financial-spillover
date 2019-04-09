import random
from functions.port_opt import *
from functions.asset_demands import *
from functions.ex_agent_asset_demands import *
from functions.balance_sheet_adjustments import *
from functions.stochasticprocess import *
from functions.expectation_formation import *
from functions.market_mechanism import *
from functions.profits_and_payouts import *
from functions.measurement import *
from functions.initialize_agents import simulated_portfolio_returns_one_country
from num_opt_pricing import *
import numpy as np
from scipy.optimize import minimize


def one_country_model(portfolios, currencies, parameters, exogenous_agents, funds, seed):
    """
    Koziol, Riedler & Schasfoort Agent-based simulation model of financial spillovers
    :param portfolios: list of asset portfolio objects
    :param currencies: list which contains the currency (single currency in this model)
    :param parameters: Object which contains all the parameters
    :param exogenous_agents: list which contains the central bank and underwriter agents
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
    # 3 simulate historical returns for portfolios & currencies:
    simulated_nominal_returns, TS_default_rates, fundamental_default_rate_expectation = simulated_portfolio_returns_one_country(
        portfolios, parameters, seed, default_rates=True)
    for c in currencies:
        simulated_nominal_returns.append(
            [c.par.nominal_interest_rate for t in range(parameters["end_day"] - parameters["start_day"])])

    ##############################################################################################################
    ############################################### DAY LOOP #####################################################
    ##############################################################################################################
    for day in range(parameters['start_day'], parameters['end_day']):
        # 1 update fund default expectations
        for fund in funds:
            pass

        # previous price is the input price
        x0 = np.ones(len(portfolios) + 1)
        for idx, a in enumerate(portfolios):
            x0[idx] = a.var.price

        res = minimize(optimal_asset_prices_one_country, x0, args=(funds, portfolios, currencies, parameters, exogenous_agents, day),
                       method='nelder-mead', options={'xtol': conv_bound / 1000, 'disp': True})

        # set the price of the portfolio's equal to the optimal prices
        for idx, a in enumerate(portfolios):
            # id_a = int(filter(str.isdigit, str(a)))
            a.var.price = res[idx]

        for fund in funds:
            # shareholder dividends and fund profits TODO change to
            fund.var.profits, \
            fund.var.losses, \
            fund.var.redeemable_shares, \
            fund.var.payouts = profit_and_payout_oc(fund, portfolios, currencies, parameters)  # TODO debug

            # Expectation formation
            fund.var.ewma_delta_prices, fund.exp.prices = price_expectations(fund, portfolios)  # TODO debug

            fund.exp.returns = return_expectations_oc(fund, portfolios, currencies, parameters)  # TODO update

            tau = 1

            # compute the weights of optimal balance sheet positions
            fund.var.weights = portfolio_optimization_KT(fund, day, tau)

            # intermediate cash position resulting from interest payments, payouts, maturing and defaulting assets
            fund.var.currency_inventory = cash_inventory(fund, portfolios, currencies)  # TODO debug

            # compute demand for balance sheet positions
            fund.var.asset_demand, fund.var.currency_demand = asset_demand_oc(fund, portfolios,
                                                                              currencies)  # TODO debug

        for ex in exogenous_agents:
            exogenous_agents[ex].var.asset_demand = ex_agent_asset_demand(ex, exogenous_agents, portfolios)

        ##########################################################################################################################
        ############################################## BALANCE SHEET ADJUSTMENT ##################################################
        ###########################################################################################################################

        # updating the covariance matrices
        if abs(portfolios[0].var.price/portfolios[0].var_previous.price-1) < 0.01:
            for fund in funds:
                fund.var.ewma_returns, fund.var.covariance_matrix, fund.var.hypothetical_returns = covariance_estimate(fund,  environment, previous_local_currency_returns[fund], inflation_shock)

        #computing new asset and cash positions
        excess_demand, pi, nu = asset_excess_demand_and_correction_factors(funds, portfolios, currencies, exogenous_agents)

         # trading
        for fund in funds:
            fund.var.assets = fund_asset_adjustments(fund, portfolios, excess_demand, pi, nu)
            fund.var.currency_inventory = fund_cash_inventory_adjustment(fund, portfolios, currencies)
            temp, fund.var.currency_demand = asset_demand(fund, portfolios, currencies, environment)

        for ex in exogenous_agents:
            exogenous_agents[ex].var.assets = ex_asset_adjustments(ex, portfolios, excess_demand, pi, nu, exogenous_agents)

        for fund in funds:
            fund.var.currency_demand = cash_demand_correction(fund, currencies,environment)

        nuC, piC, excess_demandC = cash_excess_demand_and_correction_factors(funds, currencies, exogenous_agents)

        for fund in funds:
            fund.var.currency = fund_cash_adjustments(nuC, piC, excess_demandC, currencies, fund)

        exogenous_agents["fx_interventionist"].var.currency = fx_interventionist_cash_adjustment(exogenous_agents["fx_interventionist"], nuC, piC, excess_demandC, currencies)

    return portfolios, currencies, environment, exogenous_agents, funds, data_t



