"""Main model"""
from __future__ import division
import copy
import pickle
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


def HAPB_model(portfolios, currencies, environment, exogeneous_agents, funds, seed, obj_label, saving_params):
    """
    Koziol, Riedler & Schasfoort Agent-based simulation model of financial spillovers
    :param portfolios: list of Asset objects
    :param currencies: list of Currency objects
    :param environment: object which contains parameters
    :param exogeneous_agents: list which contains the central bank and the underwriter agent
    :param funds: list of Fund objects
    :param seed: integer used to seed the random number generator
    :return: lists of assets, funds
    """
    random.seed(seed)
    np.random.seed(seed)

    ######################################################################
    ############### INITIALIZING MEASUREMENTS#############################
    ######################################################################
    deltas = {"Delta_" + str(i): 0 for i in portfolios}
    deltas["Delta_FX"] = 0
    data = initdatadict(funds, portfolios, currencies, environment, deltas ) # create tau data dictionary
    data_t = copy.deepcopy(data) # create t data dictionary

    ##################################################################################
    ###################### COMPUTING STOCHASTIC PROCESSES ############################
    ##################################################################################
    # calculating stochastic components default
    days = environment.par.global_parameters["end_day"]
    default_rates, fundamental_default_rate_expectation, shock_processes = stochastic_timeseries(environment.par.global_parameters, portfolios, days, seed)

    # initial default expectations
    noise = {}
    idiosyncratic_default_rate_noise = {}
    for j,fund in enumerate(funds):
        for i,a in enumerate(portfolios):
            random.seed(seed + j + i)
            np.random.seed(seed + j + i)
            noise[a]=[np.random.normal(0, fund.par.news_evaluation_error) for idx in range(days)]
            fund.exp.default_rates[a]=fundamental_default_rate_expectation[a][environment.par.global_parameters['start_day']-1]
        idiosyncratic_default_rate_noise[fund]=noise
    ####################################################################################
    ####################################################################################
    # creating individual intensity parameters
    for a in portfolios: #TODO: this should be taken care of in the initialization
        try:
            a.par.change_intensity
        except AttributeError:
            a.par.change_intensity = environment.par.global_parameters['p_change_intensity']

    ##############################################################################################################
    ############################################### DAY LOOP #####################################################
    ##############################################################################################################
    for day in range(environment.par.global_parameters['start_day'], environment.par.global_parameters['end_day']):
        if day >= 20:
            environment.par.global_parameters["cov_memory"]=0.001

        # these two variables are needed for the pricing algorithm
        var = copy.copy(portfolios)
        #var.append("FX")
        var_t1 = []

        for row in environment.var.fx_rates.index:
            for col in environment.var.fx_rates.columns:
                environment.var.ewma_fx_rates.loc[row, col] = compute_ewma(environment.var.fx_rates.loc[row, col], environment.var.ewma_fx_rates.loc[row, col], 0) # TODO: the last variable needs to be a parameter

        ######################################################################################
        ################ UPDATING THE STOCHASTIC SHOCK VARIABLES #############################
        #######################################################################################
        # initialise intraday prices at current price
        delta_news = {}
        fundamental_default_rates = {}

        # update default events
        for a in portfolios:
            delta_news[a] = log(fundamental_default_rate_expectation[a][day]) - log(fundamental_default_rate_expectation[a][day-1])
            fundamental_default_rates[a] = fundamental_default_rate_expectation[a][day]
            a.var.default_rate = default_rates[a][day]

        default_expectation_noise = {}
        for f in funds:
            default_expectation_noise[f] = {a: idiosyncratic_default_rate_noise[f][a][day] for a in portfolios}

        todays_shocks = {i: shock_processes[i][day] for i in shock_processes}
        fx_shock = todays_shocks["fx_shock"]

        inflation_shock = {}
        for key in todays_shocks:
            if key.split("_")[1] == "inflation":
                inflation_shock[key] = todays_shocks[key]

        # calculate expected default rates
        previous_return_exp = {} #TODO: This should be done when passing all other values to "var_previous
        previous_cons_returns = {}
        previous_local_currency_returns = {}

        for fund in funds:
            fund.exp.default_rates = dr_expectations(fund, portfolios, delta_news, fundamental_default_rates, default_expectation_noise[fund])
            previous_return_exp[fund] = fund.exp.returns.copy() # TODO: This should be done when passing all other values to "var_previous
            previous_cons_returns[fund] = fund.exp.cons_returns.copy()
            previous_local_currency_returns[fund] = fund.exp.local_currency_returns

        ###########################################################
        ############# RESETTING INTRADAY PARAMETERS ###############
        ###########################################################
        convergence=False
        asset_market_convergence = 0
        intraday_over=False
        tau=0
        Deltas = {}

        # resetting intensity adjustment parameters
        jump_counter = {a:0 for a in portfolios}
        jump_counter.update({"FX": 0})
        no_jump_counter = {a:0 for a in portfolios}
        no_jump_counter.update({"FX": 0})
        test_sign={a:0 for a in portfolios}
        test_sign.update({"FX": 0})

        ###################################################################################################################
        ################################################ INTRADAY LOOP ####################################################
        ###################################################################################################################
        def intraday_loop(asset_and_fx_prices):
            """Simulate the intra-day events"""
            # init exchange rates from function
            fx_rate = asset_and_fx_prices[0]
            combinations = []

            for column in range(len(environment.var.fx_rates.index)):
                row = 0

                while row < column:
                    combination_tuple = (environment.var.fx_rates.index[row], environment.var.fx_rates.columns[column])
                    row = row + 1
                    combinations.append(combination_tuple)

            for el in combinations:
                environment.var.fx_rates.loc[el[0]][el[1]] = fx_rate
                environment.var.fx_rates.loc[el[1]][el[0]] = 1 / fx_rate

            # initialise prices
            for idx, a in enumerate(portfolios):
                a.var.price = fx_rate[idx + 1] # set prices of all portfolio assets

            # calculate fund expectations TODO pick up here
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

                fund.exp.local_currency_returns, fund.exp.cons_returns, fund.exp.returns = return_expectations(fund, portfolios, currencies, environment)

                # compute the weights of optimal balance sheet positions
                fund.var.weights = portfolio_optimization_KT(fund, day, tau)

                # intermediate cash position resulting from interest payments, payouts, maturing and defaulting assets
                fund.var.currency_inventory = cash_inventory(fund, portfolios, currencies)

                # compute demand for balance sheet positions
                fund.var.asset_demand, fund.var.currency_demand = asset_demand(fund, portfolios, currencies, environment)

            for ex in exogeneous_agents:
                exogeneous_agents[ex].var.asset_demand = ex_agent_asset_demand(ex, exogeneous_agents, portfolios )

            for cur in currencies:
                #TODO what is this?
                if asset_market_convergence == len(portfolios):
                    exogeneous_agents["fx_interventionist"].var.currency_demand[cur] = 0

            # fill in excess demand
            total_excess_demand = []

            return total_excess_demand




        while intraday_over == False:
            tau += 1
            environment.var.tau = tau

            ############################################################################
            ################ SHOCKING FX RATES AT THE END OF A PERIOD ##################
            ############################################################################
            if convergence == True:
                intraday_over = True
                #environment, Deltas = shock_FX(portfolios, environment, exogeneous_agents, funds, currencies, fx_shock)
            #############################################################################
            #############################################################################



            # Update prices if convergence has not been achieved yet
            if not intraday_over:
                portfolios, environment, Deltas = update_market_prices_and_fx(portfolios, currencies, environment, exogeneous_agents, funds, var)

            # check for convergece of asset and fx market
            conv_bound = environment.par.global_parameters['conv_bound']
            convergence, asset_market_convergence, convergence_condition = check_convergence(Deltas, conv_bound, portfolios, tau)

            # jumps only count when they are caused by a change in the price or fx
            jump_counter, no_jump_counter, test_sign, environment = I_intensity_parameter_adjustment(
                    jump_counter, no_jump_counter, test_sign, Deltas, convergence_condition, environment,var_t1)

            var_t1 = var

            if tau == 2000 and len(var)> len(portfolios): #after 2000 periods without convergence, stop simultaneous pricing
                print('joined pricing failed on day ', day, 'in iteration ', tau)
                var = copy.copy(portfolios)
            if asset_market_convergence == len(portfolios) and len(var) <= len(portfolios):
                var.append("FX")
                for p in portfolios:
                    p.var.price_pfx = p.var.price

            # print ("day:",day,"tau:",tau, convergence, Deltas)

            # calculating and printing degree(in percent) to which the convergence bound is reached. Values <= zero need to be achieved
            list_DeltasA=[abs(Deltas[a]) for a in portfolios]
            mean_DA = ((np.mean(np.array(list_DeltasA))/conv_bound)-1)*100
            max_DA =  ((np.max(np.array(list_DeltasA))/conv_bound)-1)*100
            FX_DA = ((abs(np.array(Deltas['FX']))/conv_bound)-1)*100
            print ("day:", day, "tau:", tau, "mean_A:", mean_DA, 'max_A:', max_DA, 'FX:', FX_DA)


        ##########################################################################################################################
        ############################################## BALANCE SHEET ADJUSTMENT ##################################################
        ###########################################################################################################################

        # updating the covariance matrices
        for fund in funds:
            fund.var.ewma_returns, fund.var.covariance_matrix, fund.var.hypothetical_returns = covariance_estimate(fund,  environment, previous_local_currency_returns[fund], inflation_shock)
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
        nuC, piC, excess_demandC = cash_excess_demand_and_correction_factors(funds, currencies,exogeneous_agents)

        for fund in funds:
            fund.var.currency = fund_cash_adjustments(nuC, piC, excess_demandC, currencies, fund)
            #exogeneous_agents["fx_interventionist"].var.currency = fx_interventionist_cash_adjustment(exogeneous_agents["fx_interventionist"], nuC, piC, excess_demandC, currencies)

        # update previous variables
        for fund in funds:
            fund.var_previous = copy_agent_variables(fund.var)

        for portfolio in portfolios:
            portfolio.var_previous = copy.copy(portfolio.var)

        environment.var_previous = copy_env_variables(environment.var)
        exogeneous_agents['central_bank_domestic'].var_previous = copy_cb_variables(exogeneous_agents['central_bank_domestic'].var)
        exogeneous_agents['underwriter'].var_previous = copy_underwriter_variables(exogeneous_agents['underwriter'].var)

        # saving objects
        if day >= saving_params["time"]:
            file_name = saving_params["path"] + '/objects_day_' + str(day) + "_seed_" + str(seed) + "_" + obj_label + '.pkl'
            save_objects = open(file_name, 'wb')
            list_of_objects = [portfolios, currencies, environment, exogeneous_agents, funds, seed, obj_label]
            pickle.dump(list_of_objects, save_objects)
            save_objects.close()

    return portfolios, currencies, environment, exogeneous_agents, funds, data_t


def HAPB_model_old(portfolios, currencies, environment, exogeneous_agents, funds, seed, obj_label, saving_params):
    """
    Koziol, Riedler & Schasfoort Agent-based simulation model of financial spillovers
    :param portfolios: list of Asset objects
    :param currencies: list of Currency objects
    :param environment: object which contains parameters
    :param exogeneous_agents: list which contains the central bank and the underwriter agent
    :param funds: list of Fund objects
    :param seed: integer used to seed the random number generator
    :return: lists of assets, funds
    """
    random.seed(seed)
    np.random.seed(seed)

    ######################################################################
    ############### INITIALIZING MEASUREMENTS#############################
    ######################################################################
    deltas = {"Delta_" + str(i): 0 for i in portfolios}
    deltas["Delta_FX"] = 0
    data = initdatadict(funds, portfolios, currencies, environment, deltas ) # create tau data dictionary
    data_t = copy.deepcopy(data) # create t data dictionary

    ##################################################################################
    ###################### COMPUTING STOCHASTIC PROCESSES ############################
    ##################################################################################
    # calculating stochastic components default
    days = environment.par.global_parameters["end_day"]
    default_rates, fundamental_default_rate_expectation, shock_processes = stochastic_timeseries(environment.par.global_parameters, portfolios, days, seed)

    # initial default expectations
    noise = {}
    idiosyncratic_default_rate_noise = {}
    for j,fund in enumerate(funds):
        for i,a in enumerate(portfolios):
            random.seed(seed + j + i)
            np.random.seed(seed + j + i)
            noise[a]=[np.random.normal(0, fund.par.news_evaluation_error) for idx in range(days)]
            fund.exp.default_rates[a]=fundamental_default_rate_expectation[a][environment.par.global_parameters['start_day']-1]
        idiosyncratic_default_rate_noise[fund]=noise
    ####################################################################################
    ####################################################################################
    # creating individual intensity parameters
    for a in portfolios: #TODO: this should be taken care of in the initialization
        try:
            a.par.change_intensity
        except AttributeError:
            a.par.change_intensity = environment.par.global_parameters['p_change_intensity']

    ##############################################################################################################
    ############################################### DAY LOOP #####################################################
    ##############################################################################################################
    for day in range(environment.par.global_parameters['start_day'], environment.par.global_parameters['end_day']):
        if day >= 20:
            environment.par.global_parameters["cov_memory"]=0.001

        # these two variables are needed for the pricing algorithm
        var = copy.copy(portfolios)
        #var.append("FX")
        var_t1 = []

        for row in environment.var.fx_rates.index:
            for col in environment.var.fx_rates.columns:
                environment.var.ewma_fx_rates.loc[row, col] = compute_ewma(environment.var.fx_rates.loc[row, col], environment.var.ewma_fx_rates.loc[row, col], 0) # TODO: the last variable needs to be a parameter

        ######################################################################################
        ################ UPDATING THE STOCHASTIC SHOCK VARIABLES #############################
        #######################################################################################
        # initialise intraday prices at current price
        delta_news = {}
        fundamental_default_rates = {}

        # update default events
        for a in portfolios:
            delta_news[a] = log(fundamental_default_rate_expectation[a][day]) - log(fundamental_default_rate_expectation[a][day-1])
            fundamental_default_rates[a] = fundamental_default_rate_expectation[a][day]
            a.var.default_rate = default_rates[a][day]

        default_expectation_noise = {}
        for f in funds:
            default_expectation_noise[f] = {a: idiosyncratic_default_rate_noise[f][a][day] for a in portfolios}

        todays_shocks = {i: shock_processes[i][day] for i in shock_processes}
        fx_shock = todays_shocks["fx_shock"]

        inflation_shock = {}
        for key in todays_shocks:
            if key.split("_")[1] == "inflation":
                inflation_shock[key] = todays_shocks[key]

        # calculate expected default rates
        previous_return_exp = {} #TODO: This should be done when passing all other values to "var_previous
        previous_cons_returns = {}
        previous_local_currency_returns = {}

        for fund in funds:
            fund.exp.default_rates = dr_expectations(fund, portfolios, delta_news, fundamental_default_rates, default_expectation_noise[fund])
            previous_return_exp[fund] = fund.exp.returns.copy() # TODO: This should be done when passing all other values to "var_previous
            previous_cons_returns[fund] = fund.exp.cons_returns.copy()
            previous_local_currency_returns[fund] = fund.exp.local_currency_returns

        ###########################################################
        ############# RESETTING INTRADAY PARAMETERS ###############
        ###########################################################
        convergence=False
        asset_market_convergence = 0
        intraday_over=False
        tau=0
        Deltas = {}

        # resetting intensity adjustment parameters
        jump_counter = {a:0 for a in portfolios}
        jump_counter.update({"FX": 0})
        no_jump_counter = {a:0 for a in portfolios}
        no_jump_counter.update({"FX": 0})
        test_sign={a:0 for a in portfolios}
        test_sign.update({"FX": 0})

        ###################################################################################################################
        ################################################ INTRADAY LOOP ####################################################
        ###################################################################################################################
        while intraday_over == False:
            tau += 1
            environment.var.tau = tau

            ############################################################################
            ################ SHOCKING FX RATES AT THE END OF A PERIOD ##################
            ############################################################################
            if convergence == True:
                intraday_over = True
                #environment, Deltas = shock_FX(portfolios, environment, exogeneous_agents, funds, currencies, fx_shock)
            #############################################################################
            #############################################################################

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

                fund.exp.local_currency_returns, fund.exp.cons_returns, fund.exp.returns = return_expectations(fund, portfolios, currencies, environment)

                # compute the weights of optimal balance sheet positions
                fund.var.weights = portfolio_optimization_KT(fund, day, tau)
                #print fund.var.weights , '\n', x

                # intermediate cash position resulting from interest payments, payouts, maturing and defaulting assets
                fund.var.currency_inventory = cash_inventory(fund, portfolios, currencies)

                # compute demand for balance sheet positions
                fund.var.asset_demand, fund.var.currency_demand = asset_demand(fund, portfolios, currencies, environment)

            for ex in exogeneous_agents:
                exogeneous_agents[ex].var.asset_demand = ex_agent_asset_demand(ex, exogeneous_agents, portfolios )

            for cur in currencies:
                if asset_market_convergence == len(portfolios):
                    exogeneous_agents["fx_interventionist"].var.currency_demand[cur]=0

            # Update prices if convergence has not been achieved yet
            if intraday_over == False:
                portfolios, environment, Deltas = update_market_prices_and_fx(portfolios, currencies, environment, exogeneous_agents, funds, var)

            # check for convergece of asset and fx market
            conv_bound = environment.par.global_parameters['conv_bound']
            convergence, asset_market_convergence, convergence_condition = check_convergence(Deltas, conv_bound, portfolios, tau)

            # jumps only count when they are caused by a change in the price or fx
            jump_counter, no_jump_counter, test_sign, environment = I_intensity_parameter_adjustment(
                    jump_counter, no_jump_counter, test_sign, Deltas, convergence_condition, environment,var_t1)

            var_t1 = var

            if tau == 2000 and len(var)> len(portfolios): #after 2000 periods without convergence, stop simultaneous pricing
                print('joined pricing failed on day ', day, 'in iteration ', tau)
                var = copy.copy(portfolios)
            if asset_market_convergence == len(portfolios) and len(var)<= len(portfolios):
                var.append("FX")
                for p in portfolios:
                    p.var.price_pfx=p.var.price

            # print ("day:",day,"tau:",tau, convergence, Deltas)

            # calculating and printing degree(in percent) to which the convergence bound is reached. Values <= zero need to be achieved
            list_DeltasA=[abs(Deltas[a]) for a in portfolios]
            mean_DA = ((np.mean(np.array(list_DeltasA))/conv_bound)-1)*100
            max_DA =  ((np.max(np.array(list_DeltasA))/conv_bound)-1)*100
            FX_DA = ((abs(np.array(Deltas['FX']))/conv_bound)-1)*100
            print ("day:", day, "tau:", tau, "mean_A:", mean_DA, 'max_A:', max_DA, 'FX:', FX_DA)

            # saving objects when there is no convergence (for diagnostic purpose)
            if tau > 10000:
                print('convergence failed on day ', day)
                file_name = saving_params["path"] + '/!objects_nonConv_day' + str(day) + '.pkl'
                save_objects = open(file_name, 'wb')
                list_of_objects = [portfolios, currencies, environment, exogeneous_agents, funds, seed]
                pickle.dump(list_of_objects, save_objects)
                save_objects.close()

        ##########################################################################################################################
        ############################################## BALANCE SHEET ADJUSTMENT ##################################################
        ###########################################################################################################################

        # updating the covariance matrices
        for fund in funds:
            fund.var.ewma_returns, fund.var.covariance_matrix, fund.var.hypothetical_returns = covariance_estimate(fund,  environment, previous_local_currency_returns[fund], inflation_shock)
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
        nuC, piC, excess_demandC = cash_excess_demand_and_correction_factors(funds, currencies,exogeneous_agents)

        for fund in funds:
            fund.var.currency = fund_cash_adjustments(nuC, piC, excess_demandC, currencies, fund)
            #exogeneous_agents["fx_interventionist"].var.currency = fx_interventionist_cash_adjustment(exogeneous_agents["fx_interventionist"], nuC, piC, excess_demandC, currencies)

        # update previous variables
        for fund in funds:
            fund.var_previous = copy_agent_variables(fund.var)

        for portfolio in portfolios:
            portfolio.var_previous = copy.copy(portfolio.var)

        environment.var_previous = copy_env_variables(environment.var)
        exogeneous_agents['central_bank_domestic'].var_previous = copy_cb_variables(exogeneous_agents['central_bank_domestic'].var)
        exogeneous_agents['underwriter'].var_previous = copy_underwriter_variables(exogeneous_agents['underwriter'].var)

        # saving objects
        if day >= saving_params["time"]:
            file_name = saving_params["path"] + '/objects_day_' + str(day) + "_seed_" + str(seed) + "_" + obj_label + '.pkl'
            save_objects = open(file_name, 'wb')
            list_of_objects = [portfolios, currencies, environment, exogeneous_agents, funds, seed, obj_label]
            pickle.dump(list_of_objects, save_objects)
            save_objects.close()

    return portfolios, currencies, environment, exogeneous_agents, funds, data_t
