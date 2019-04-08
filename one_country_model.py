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
        # 1 update default events
        print(1)
        # 2 update fund default expectations
        for fund in funds:
            pass
        # 3 RESETTING INTRADAY PARAMETERS
        convergence = False
        asset_market_convergence = 0
        intraday_over = False
        tau = 0
        Deltas = {}

        jump_counter = {a: 0 for a in portfolios}
        no_jump_counter = {a: 0 for a in portfolios}
        test_sign = {a: 0 for a in portfolios}

        ###################################################################################################################
        ################################################ INTRADAY LOOP ####################################################
        ###################################################################################################################
        while intraday_over == False:
            tau += 1
            if convergence:
                intraday_over = True

            for fund in funds:
                # shareholder dividends and fund profits
                fund.var.profits, \
                fund.var.cons_profits, \
                fund.var.losses, \
                fund.var.redeemable_shares, \
                fund.var.payouts = profit_and_payout(fund, portfolios, currencies, environment)

                # Expectation formation
                fund.var.ewma_delta_prices, \
                fund.var.ewma_delta_fx, \
                fund.exp.prices, \
                fund.exp.exchange_rates = price_fx_expectations(fund, portfolios, currencies, environment)

                fund.exp.exchange_rates, fund.exp.exchange_rate_anchor = anchored_FX_expectations(fund, environment, fx_shock)

                fund.exp.returns = return_expectations(fund, portfolios, currencies, environment)

                # compute the weights of optimal balance sheet positions
                #fund.var.weights  = portfolio_optimization(fund)
                fund.var.weights = portfolio_optimization_KT(fund,day, tau)

                # intermediate cash position resulting from interest payments, payouts, maturing and defaulting assets
                fund.var.currency_inventory = cash_inventory(fund, portfolios, currencies)

                # compute demand for balance sheet positions
                fund.var.asset_demand, fund.var.currency_demand = asset_demand(fund, portfolios, currencies, environment)

            for ex in exogenous_agents:
                exogenous_agents[ex].var.asset_demand = ex_agent_asset_demand(ex, exogenous_agents, portfolios)

            # Update prices if convergence has not been achieved yet
            if not intraday_over:
                pre_prices = {}
                for a in portfolios:
                    pre_prices.update({a: a.var.price})

                portfolios, environment, Deltas = update_market_prices_and_fx(portfolios, currencies, environment, exogenous_agents, funds, var)

            # check for convergece of asset and fx market
            conv_bound = environment.par.global_parameters['conv_bound']
            convergence, asset_market_convergence, convergence_condition = check_convergence(Deltas, conv_bound, portfolios, tau)

            jump_counter, no_jump_counter, test_sign, environment = I_intensity_parameter_adjustment(
                    jump_counter, no_jump_counter, test_sign, Deltas, convergence_condition, environment, var_t1)

            update = 0
            if var_t1 == []:
                var_t1 = [v for v in var]
                update = 1
            if len(var) > 1:
                var_t1 = [v for v in var]

            h_var = []
            for i in jump_counter:
                if jump_counter[i] == 10:  # and convergence_condition[i]==False:
                    h_var.append(i)
            if len(h_var) > 0 and update == 0:
                var = [np.random.permutation(h_var)[0]]
                var_t1 = []
            else:
                var = [v for v in var_original]

                # calculating and printing degree(in percent) to which the convergence bound is reached. Values <= zero need to be achieved
                list_DeltasA = [abs(Deltas[a]) for a in portfolios]
                mean_DA = np.mean(np.array(list_DeltasA))
                max_DA = np.max(np.array(list_DeltasA))
                FX_DA = (np.array(Deltas['FX']))

                ####### PRINT STATEMENTS GOOD FOR IMMEDIATE TROUBLE SHOOTING
                # print ("day:", day, "tau:", tau, "mean_A:", mean_DA, 'max_A:', max_DA, 'FX:', FX_DA)
                # print([portfolios[0].par.change_intensity,portfolios[1].par.change_intensity,portfolios[2].par.change_intensity,portfolios[3].par.change_intensity, environment.par.global_parameters["fx_change_intensity"]])
                # print([(Deltas[a]) for a in portfolios])
                # print([a.var.price for a in portfolios])

                # saving objects when there is no convergence (for diagnostic purpose)
                if tau > 5000:
                    print('convergence failed on day ', day)

                NO = 0
                # try numerical optimization
                if NO == 1:
                    # storing prices and fx before numerical optimization
                    pre_prices = {}
                    for a in portfolios:
                        pre_prices.update({a: a.var.price})
                    pre_fx = environment.var.fx_rates.copy()

                    x0 = np.ones(len(portfolios) + 1)
                    for a in portfolios:
                        id_a = int(filter(str.isdigit, str(a)))
                        x0[id_a] = a.var.price
                    x0[-1] = environment.var.fx_rates.iloc[0][1]

                    res = minimize(NOP, x0,
                                   args=(funds, portfolios, currencies, environment, exogenous_agents, day, fx_shock),
                                   method='nelder-mead', options={'xtol': conv_bound / 1000, 'disp': True})

                    update_prices = 1
                    if update_prices == 0:
                        for a in portfolios:
                            a.var.price = pre_prices[a]

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



