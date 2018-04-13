"""Main model"""

import copy
import pickle
from functions.port_opt import *
from functions.asset_demands import *
from functions.ex_agent_asset_demands import *
from functions.balance_sheet_adjustments import *
from functions.stochasticprocess import *
from functions.expectation_formation import *
from functions.market_mechanism import *
from functions.profits_and_payouts import *
from functions.show import *
from functions.supercopy import *

from functions.measurement import *


def spillover_model(portfolios, currencies, environment, exogeneous_agents, funds,  seed):
    """
    Koziol, Riedler & Schasfoort Agent-based simulation model of financial spillovers
    :param assets: list of Asset objects
    :param funds: list of Fund objects
    :param days: integer amount of days over which the simulation will take place
    :param seed: integer used to seed the random number generator
    :return: lists of assets, funds
    """
    random.seed(seed)
    np.random.seed(seed)

    # defining start days
    if 'start_day' not in environment.par.global_parameters:
        environment.par.global_parameters['start_day'] = 1
        environment.par.global_parameters['end_day'] = environment.par.global_parameters["days"]

    #Measurements
    deltas = {"Delta_" + str(i): 0 for i in portfolios}
    deltas["Delta_FX"] = 0

    data = initdatadict(funds, portfolios, currencies, environment, deltas ) # create tau data dictionary
    data_t = copy.deepcopy(data) # create t data dictionary


    # calculating stochastic components default
    default_rates, fundamental_default_rate_expectation = exogenous_defaults(environment, portfolios)


    # initial default expectations
    for fund in funds:
        for a in portfolios:
            fund.exp.default_rates[a]=fundamental_default_rate_expectation[a][0]

    # Random fx noise
    fx_shock = [ np.random.normal(0, environment.par.global_parameters["fx_shock_std"]) for i in range(environment.par.global_parameters["days"]) ]

    # pricing with returns instead of prices requires an initialized return (NOTE, THIS IS A PRACTICAL MODELING CHOICE WITH NO ECONOMIC MEANING)
    for a in portfolios:
        a.var.aux_ret = convert_P2R(a,a.var.price)
        if a.var.aux_ret<=0:
            a.var.aux_ret=0.0001

    # creating individual intensity parameters
    for a in portfolios:
        try:
            a.par.change_intensity
        except AttributeError:
            a.par.change_intensity = environment.par.global_parameters['p_change_intensity']





    for day in range(environment.par.global_parameters['start_day'], environment.par.global_parameters['end_day']):
        # initialise intraday prices at current price
        delta_news = {}
        fundamental_default_rates = {}

        # update default events
        for a in portfolios:
            delta_news[a] = log(fundamental_default_rate_expectation[a][day]) - log(fundamental_default_rate_expectation[a][day-1])
            fundamental_default_rates[a] = fundamental_default_rate_expectation[a][day]
            a.var.default_rate = default_rates[a][day]

        # calculate expected default rates
        previous_return_exp = {}

        random.seed(seed+day)
        np.random.seed(seed+day)
        for fund in funds:
            fund.exp.default_rates = dr_expectations(fund, portfolios, delta_news, fundamental_default_rates)
            previous_return_exp[fund]=fund.exp.returns.copy() # needed to compute the covariance matrix

        convergence=False
        intraday_over=False


        tau=0

        # resetting intensity adjustment parameters
        jump_counter = {a:0 for a in portfolios}
        jump_counter.update({"FX": 0})
        no_jump_counter = {a:0 for a in portfolios}
        no_jump_counter.update({"FX": 0})
        test_sign={a:0 for a in portfolios}
        test_sign.update({"FX": 0})

        while intraday_over == False:
            tau += 1

            if convergence == True:
                intraday_over = True

                # shocking prices and exchange rates
                if intraday_over == True:
                    Delta_Demand = {}
                    lastP={a: a.par.change_intensity for a in portfolios}
                    lastFX=environment.par.global_parameters['fx_change_intensity']
                    for a in portfolios:
                        a.par.change_intensity = 0
                    environment.par.global_parameters['fx_change_intensity'] = 0
                    for a in portfolios:
                        a.var.price, a.var.aux_ret, Delta_str, delta_demand = price_adjustment(portfolios, environment,
                                                                                               exogeneous_agents, funds,
                                                                                               a)
                        Delta_Demand.update({a: delta_demand})

                    environment.var.fx_rates.iloc[0, 1] = environment.var.fx_rates.iloc[0, 1] * (1 + fx_shock[day])
                    environment.var.fx_rates.iloc[1, 0] = 1 / environment.var.fx_rates.iloc[0, 1]
                    environment.var.fx_rates, Delta_Capital = fx_adjustment(portfolios, currencies, environment, funds)

                    for a in portfolios:
                        a.par.change_intensity = lastP[a]
                    environment.par.global_parameters['fx_change_intensity'] = lastFX


            for fund in funds:
                # shareholder dividends and fund profits 
                fund.var.profits, \
                fund.var.losses, \
                fund.var.redeemable_shares, \
                fund.var.payouts = profit_and_payout(fund, portfolios, currencies, environment)
                # 1 Expectation formation
                fund.var.ewma_delta_prices, \
                fund.var.ewma_delta_fx, \
                fund.exp.prices, \
                fund.exp.exchange_rates = price_fx_expectations(fund, portfolios, currencies, environment)
                fund.exp.returns = return_expectations(fund, portfolios, currencies, environment)
                fund.var.ewma_returns, fund.var.covariance_matrix, fund.var.hypothetical_returns = covariance_estimate(fund,  environment, previous_return_exp[fund])

                # compute the weights of optimal balance sheet positions
                fund.var.weights = portfolio_optimization(fund)

                # intermediate cash position resulting from interest payments, payouts, maturing and defaulting assets
                fund.var.currency_inventory = cash_inventory(fund, portfolios, currencies)

                # compute demand for balance sheet positions
                fund.var.asset_demand, fund.var.currency_demand = asset_demand(fund, portfolios, currencies, environment)

            for ex in exogeneous_agents:
                exogeneous_agents[ex].var.asset_demand = ex_agent_asset_demand(ex, exogeneous_agents, portfolios )


            if intraday_over == False:
                Delta_Demand = { }
                for a in portfolios:
                    a.var.price, a.var.aux_ret, Delta_str, delta_demand  = price_adjustment(portfolios, environment, exogeneous_agents, funds, a)
                    Delta_Demand.update({a: delta_demand})
                environment.var.fx_rates, Delta_Capital = fx_adjustment(portfolios, currencies, environment , funds)

            Deltas = {}
            Deltas.update(Delta_Demand)
            Deltas.update({"FX": Delta_Capital})

            convergence_bound = 0.001
            convergence = sum(abs(Deltas[i])<convergence_bound for i in Deltas)==len(Deltas) and tau >30

            jump_counter, no_jump_counter, test_sign, environment = intensity_parameter_adjustment(jump_counter, no_jump_counter, test_sign, Deltas, environment, convergence_bound)


            print ("day:",day,"tau:",tau, convergence, Deltas)
            #print ("-")
            #print(funds[0].var.asset_demand , funds[0].var.currency_demand,funds[0].exp.returns)
            #print (funds[1].var.asset_demand,funds[1].var.currency_demand, funds[1].exp.returns )
            #print (funds[0].var.hypothetical_returns, funds[0].var.covariance_matrix.iloc[2,2],funds[0].var.covariance_matrix.iloc[3,3])
            #print (funds[1].var.hypothetical_returns,funds[1].var.covariance_matrix.iloc[2,2],funds[1].var.covariance_matrix.iloc[3,3])
            #print(funds[0].var.weights)
            #print(funds[1].var.weights)
            #print("-")


            #Update intraday data points
            data = update_data(data, funds, portfolios, currencies, environment, Deltas)
            #this is where intraday simulation ends

            # saving objects when there is no convergence (for diagnostic purpose)
            if tau > 10000:
                file_name = 'data/Objects/objects_nonConv_day' + str(day) + '.pkl'
                save_objects = open(file_name, 'wb')
                list_of_objects = [portfolios, currencies, environment, exogeneous_agents, funds, seed]
                pickle.dump(list_of_objects, save_objects)
                save_objects.close()

        pd.DataFrame(data).to_csv('data' + '/' + "intraday" + "/" + "intraday_data_day_" + str(day) + ".csv")


        # balance sheet adjustment

        #computing new asset and cash positions
        excess_demand, pi, nu = asset_excess_demand_and_correction_factors(funds, portfolios, currencies, exogeneous_agents)

         # trading
        for fund in funds:
            fund.var.assets = fund_asset_adjustments(fund, portfolios, excess_demand, pi, nu)
            fund.var.currency_inventory = fund_cash_inventory_adjustment(fund, portfolios, currencies)
            temp, fund.var.currency_demand = asset_demand(fund, portfolios, currencies, environment)

        for ex in exogeneous_agents:
            exogeneous_agents[ex].var.assets = ex_asset_adjustments(ex, portfolios, excess_demand, pi, nu, exogeneous_agents)

        for fund in funds:
            fund.var.currency_demand = cash_demand_correction(fund, currencies,environment)

        nuC, piC, excess_demandC = cash_excess_demand_and_correction_factors(funds, currencies)


        for fund in funds:
            fund.var.currency = fund_cash_adjustments(nuC, piC, excess_demandC, currencies, fund)

        #debugging
        show_fund(funds[0], portfolios, currencies, environment)
        show_fund(funds[1], portfolios, currencies, environment)

        # update previous variables
        for fund in funds:
            fund.var_previous = copy_agent_variables(fund.var)

        for portfolio in portfolios:
            portfolio.var_previous = copy.copy(portfolio.var)

        environment.var_previous = copy_env_variables(environment.var)

        exogeneous_agents['central_bank_domestic'].var_previous = copy_cb_variables(exogeneous_agents['central_bank_domestic'].var)
        exogeneous_agents['underwriter'].var_previous = copy_underwriter_variables(exogeneous_agents['underwriter'].var)


        #End of day measurements
        #Update data points for day
        if convergence == True:
            #reset intraday datapoints inside value lists of data
            data = reset_intraday(data)
            #Update data_t
            data_t = update_data(data_t, funds, portfolios, currencies, environment, Deltas)

        # 4 Measurement
        pd.DataFrame(data_t).to_csv('data' + '/' + "data_t.csv")

        # saving objects
        file_name = 'data/Objects/objects_day_' + str(day) + '.pkl'
        save_objects = open(file_name, 'wb')
        list_of_objects = [portfolios, currencies, environment, exogeneous_agents, funds, seed]
        pickle.dump(list_of_objects, save_objects)
        save_objects.close()

    return portfolios, currencies, environment, exogeneous_agents, funds,  data_t