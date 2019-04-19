import random
import numpy as np
from scipy import optimize
from functions.balance_sheet_adjustments import *
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

    for day in range(parameters['start_day'], parameters['end_day'] - 1):
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
        x0 = np.ones(len(portfolios))
        for idx, a in enumerate(portfolios):
            x0[idx] = a.var.price[day - 1]

        # find equilibrium prices for assets.
        #optimal_asset_prices_one_country(x0, funds, portfolios, currencies, parameters, exogenous_agents, day)
        print(day)
        res2 = optimize.root(optimal_asset_prices_one_country, x0, args=(funds, portfolios, currencies, parameters, exogenous_agents, day), method='broyden1')
        res = res2['x']

        # set the price of the portfolio's equal to the optimal prices TODO, this is probably not nescessary as the price was already set.
        for idx, a in enumerate(portfolios):
            # id_a = int(filter(str.isdigit, str(a)))
            a.var.price[day] = res[idx]

        # use these prices to determine final expectations, weight, and demand.
        for fund in funds:
            # shareholder dividends and fund profits
            f_profits, f_losses, f_redeemable_shares, f_payouts = profit_and_payout_oc(fund, portfolios, currencies,
                                                                                       day)
            fund.var.redeemable_shares.append(f_redeemable_shares)
            for key in f_profits:
                fund.var.profits[key][day] = f_profits[key]
                if key in currencies:
                    fund.var.losses[day] = f_losses[key]
                    fund.var.payouts += f_payouts[key]

            # Expectation formation
            fund.var.ewma_delta_prices, fund_exp_prices = price_expectations(fund, portfolios, day)
            for a in fund_exp_prices:
                fund.exp.prices[a][day] = fund_exp_prices[a]

            fund_exp_returns = return_expectations_oc(fund, portfolios, currencies, day)
            for a in fund_exp_returns:
                fund.exp.returns[a][day] = fund_exp_returns[a]

            # compute the weights of optimal balance sheet positions
            fund.var.weights = portfolio_optimization_oc(fund, day)

            # intermediate cash position resulting from interest payments, payouts, maturing and defaulting assets
            fund.var.currency_inventory = cash_inventory_oc(fund, portfolios, currencies, day)  # TODO debug

            # compute demand for balance sheet positions
            fund.var.asset_demand, fund.var.currency_demand = asset_demand_oc(fund, portfolios, currencies,
                                                                              day)  # TODO debug

        for ex in exogenous_agents:
            exogenous_agents[ex].var.asset_demand = ex_agent_asset_demand_oc(ex, exogenous_agents, portfolios, day)

        ##########################################################################################################################
        ############################################## BALANCE SHEET ADJUSTMENT ##################################################
        ###########################################################################################################################

        # updating the covariance matrices TODO debug
        if abs(portfolios[0].var.price[day] / portfolios[0].var.price[day - 1] - 1) < 0.05: # 0.01
            for fund in funds:
                fund.var.ewma_returns[day], fund.var.covariance_matrix[day], fund.var.hypothetical_returns[day] = covariance_estimate_oc(fund, parameters, day)

        #computing new asset and cash positions
        excess_demand, pi, nu = asset_excess_demand_and_correction_factors(funds, portfolios, currencies, exogenous_agents)

         # trading
        for fund in funds:
            fund_assets = fund_asset_adjustments_oc(fund, portfolios, excess_demand, pi, nu, day)
            for a in fund.var.assets:
                fund.var.assets[a][day] = fund_assets[a]

            fund_currency_inventory = fund_cash_inventory_adjustment_oc(fund, portfolios, currencies, day)
            for c in fund_currency_inventory:
                fund.var.currency_inventory[c] = fund_currency_inventory[c]

            temp, fund.var.currency_demand = asset_demand_oc(fund, portfolios, currencies, day)

        for ex in exogenous_agents:
            exogenous_agents_var_assets = ex_asset_adjustments_oc(ex, portfolios, excess_demand, pi, nu, exogenous_agents, day)
            for a in exogenous_agents_var_assets:
                exogenous_agents[ex].var.assets[a][day] = exogenous_agents_var_assets[a]

        for fund in funds:
            fund.var.currency_demand = cash_demand_correction_oc(fund, currencies)

        nuC, piC, excess_demandC = cash_excess_demand_and_correction_factors_oc(funds, currencies, exogenous_agents)

        for fund in funds:
            fund_var_currency = fund_cash_adjustments(nuC, piC, excess_demandC, currencies, fund)
            for c in fund_var_currency:
                fund.var.currency[c][day] = fund_var_currency[c]

    return portfolios, currencies, exogenous_agents, funds



