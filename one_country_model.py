import random
import numpy as np
from scipy import optimize
from functions.balance_sheet_adjustments import *
from functions.initialize_agents import simulated_portfolio_returns_one_country
from num_opt_pricing import *


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

    # TODO in code below refer to noise held by agent, and fundamental dfr exp for every asset + default rates of assets themselves
    for day in range(parameters['start_day'], parameters['end_day']):
        # 1 update fund default expectations
        delta_news = {}
        fundamental_default_rates = {}

        # update default rates for all assets
        for a in portfolios:
            delta_news[a] = log(a.var.f_exp_dr[day]) - log(a.var.f_exp_dr[day - 1])
            fundamental_default_rates[a] = a.var.f_exp_dr[day]

        default_expectation_noise = {}
        for f in funds:
            default_expectation_noise[f] = {a: f.exp.exp_noise[a][day] for a in portfolios}
            f_exp_default_rates = dr_expectations_oc(f, portfolios, delta_news, fundamental_default_rates,
                                                     default_expectation_noise[f], day)
            for a in f_exp_default_rates:
                f.exp.default_rates[a][day] = f_exp_default_rates[a] #TODO check if this works

        # use previous price as input price for the pricing algorithm
        x0 = np.ones(len(portfolios))  # TODO .. + 1 is needed?
        for idx, a in enumerate(portfolios):
            x0[idx] = a.var.price[day - 1]

        # find equilibrium prices for assets.
        #optimal_asset_prices_one_country(x0, funds, portfolios, currencies, parameters, exogenous_agents, day)

        #res = optimize.fsolve(optimal_asset_prices_one_country, x0, args=(funds, portfolios, currencies, parameters, exogenous_agents, day))
        res2 = optimize.root(optimal_asset_prices_one_country, x0, args=(funds, portfolios, currencies, parameters, exogenous_agents, day), method='broyden1')

        # set the price of the portfolio's equal to the optimal prices
        for idx, a in enumerate(portfolios):
            # id_a = int(filter(str.isdigit, str(a)))
            a.var.price = res2[idx]

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



