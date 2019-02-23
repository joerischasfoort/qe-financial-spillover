"""Main model"""

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


from num_opt_pricing import *
import numpy as np
from scipy.optimize import minimize




def spillover_model(portfolios, currencies, environment, exogeneous_agents, funds,  seed,seed1, obj_label,saving_params,var):
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

    ######################################################################
    ############### INITIALIZING MEASUREMENTS#############################
    ######################################################################
    deltas = {"Delta_" + str(i): 0 for i in portfolios}
    deltas["Delta_FX"] = 0
    #data = initdatadict(funds, portfolios, currencies, environment, deltas ) # create tau data dictionary
    #data_t = copy.deepcopy(data) # create t data dictionary
    data = 0
    data_t =0

    ##################################################################################
    ###################### COMPUTING STOCHASTIC PROCESSES ############################
    ##################################################################################
    # calculating stochastic components default
    days = environment.par.global_parameters["end_day"]
    if environment.par.global_parameters["start_day"] ==1:
        default_rates, fundamental_default_rate_expectation, shock_processes = stochastic_timeseries(environment.par.global_parameters, portfolios, days, seed)
    else:
        default_rates, fundamental_default_rate_expectation, shock_processes = stochastic_timeseries_2(environment.par.global_parameters, portfolios, environment.par.global_parameters['start_day'], environment.par.global_parameters['end_day'], seed, seed1)

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

    # these two variables are needed for the pricing algorithm

    # var_t1 = []
    var_original = [v for v in var]
    var_t1 = [v for v in var]
    if "FX" in var:
        del var[var.index("FX")]


    ##############################################################################################################
    ############################################### DAY LOOP #####################################################
    ##############################################################################################################
    for day in range(environment.par.global_parameters['start_day'], environment.par.global_parameters['end_day']):

        if day >= environment.par.global_parameters["start_day"]+5:
            environment.par.global_parameters["cov_memory"]=0.001




        for row in environment.var.fx_rates.index:
            for col in environment.var.fx_rates.columns:
                environment.var.ewma_fx_rates.loc[row, col] = compute_ewma(environment.var.fx_rates.loc[row, col], environment.var.ewma_fx_rates.loc[row, col],0) # TODO: the last variable needs to be a parameter

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
            previous_return_exp[fund]=fund.exp.returns.copy() # TODO: This should be done when passing all other values to "var_previous
            previous_cons_returns[fund]=fund.exp.cons_returns.copy()
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

                fund.exp.returns = return_expectations(fund, portfolios, currencies, environment)

                # compute the weights of optimal balance sheet positions
                #fund.var.weights  = portfolio_optimization(fund)
                fund.var.weights = portfolio_optimization_KT(fund,day, tau)

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
                pre_prices = {}
                for a in portfolios:
                    pre_prices.update({a: a.var.price})

                portfolios, environment, Deltas = update_market_prices_and_fx(portfolios, currencies, environment, exogeneous_agents, funds, var)

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

            if "FX" in var and asset_market_convergence < len(portfolios) and tau<50:
                del var[var.index("FX")]

            #calculating and printing degree(in percent) to which the convergence bound is reached. Values <= zero need to be achieved
            list_DeltasA=[abs(Deltas[a]) for a in portfolios]
            mean_DA = np.mean(np.array(list_DeltasA))
            max_DA =  np.max(np.array(list_DeltasA))
            FX_DA = (np.array(Deltas['FX']))

            ####### PRINT STATEMENTS GOOD FOR IMMEDIATE TROUBLE SHOOTING 
            # print ("day:", day, "tau:", tau, "mean_A:", mean_DA, 'max_A:', max_DA, 'FX:', FX_DA)
            # print([portfolios[0].par.change_intensity,portfolios[1].par.change_intensity,portfolios[2].par.change_intensity,portfolios[3].par.change_intensity, environment.par.global_parameters["fx_change_intensity"]])
            # print([(Deltas[a]) for a in portfolios])
            # print([a.var.price for a in portfolios])


            # saving objects when there is no convergence (for diagnostic purpose)
            if tau > 5000:
                print('convergence failed on day ', day)
                file_name = saving_params["path"] + '/!objects_nonConv_day' + str(day) + '.pkl'
                save_objects = open(file_name, 'wb')
                list_of_objects = [portfolios, currencies, environment, exogeneous_agents, funds, seed]
                pickle.dump(list_of_objects, save_objects)
                save_objects.close()


            NO=0
            # try numerical optimization
            if NO==1:
                #storing prices and fx before numerical optimization
                pre_prices = {}
                for a in portfolios:
                    pre_prices.update({a: a.var.price})
                pre_fx =  environment.var.fx_rates.copy()

                x0 = np.ones(len(portfolios) + 1)
                for a in portfolios:
                    id_a = int(filter(str.isdigit, str(a)))
                    x0[id_a] = a.var.price
                x0[-1] = environment.var.fx_rates.iloc[0][1]

                res = minimize(NOP, x0, args=(funds, portfolios, currencies, environment, exogeneous_agents, day, fx_shock),
                               method='nelder-mead', options={'xtol': conv_bound/1000, 'disp': True})

                update_prices = 1
                if update_prices == 0:
                    for a in portfolios:
                        a.var.price = pre_prices[a]
                    environment.var.fx_rates = pre_fx

        ##########################################################################################################################
        ############################################## BALANCE SHEET ADJUSTMENT ##################################################
        ###########################################################################################################################

        # updating the covariance matrices
        if abs(portfolios[0].var.price/portfolios[0].var_previous.price-1) < 0.01:
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

        exogeneous_agents["fx_interventionist"].var.currency = fx_interventionist_cash_adjustment(exogeneous_agents["fx_interventionist"], nuC, piC, excess_demandC, currencies)

        # update previous variables
        for fund in funds:
            fund.var_previous = copy_agent_variables(fund.var)

        for portfolio in portfolios:
            portfolio.var_previous = copy.copy(portfolio.var)

        environment.var_previous = copy_env_variables(environment.var)

        exogeneous_agents['central_bank_domestic'].var_previous = copy_cb_variables(exogeneous_agents['central_bank_domestic'].var)
        exogeneous_agents['underwriter'].var_previous = copy_underwriter_variables(exogeneous_agents['underwriter'].var)



        # saving objects
        if day>=saving_params["time"]:
            file_name = saving_params["path"] + '/objects_day_' + str(day) + "_seed_" + str(seed) + "_" + obj_label + '.pkl'
            save_objects = open(file_name, 'wb')
            list_of_objects = [portfolios, currencies, environment, exogeneous_agents, funds, seed, obj_label]
            pickle.dump(list_of_objects, save_objects)
            save_objects.close()

    return portfolios, currencies, environment, exogeneous_agents, funds,  data_t