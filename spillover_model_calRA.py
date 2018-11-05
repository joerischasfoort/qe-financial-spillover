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
from functions.calibration_mechanism import *
from functions.profits_and_payouts import *
from functions.supercopy import *
from functions.measurement import *


from num_opt_pricing import *
import numpy as np
from scipy.optimize import minimize




def spillover_model_calRA(portfolios, currencies, environment, exogeneous_agents, funds,  seed, obj_label,saving_params,var):
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
    data = []
#
    #    data = initdatadict(funds, portfolios, currencies, environment, deltas ) # create tau data dictionary
 #   data_t = copy.deepcopy(data) # create t data dictionary
    ######################################################################
    ##### Determine directoring for saving objects and measurement########
    ######################################################################
    hex_home = '/home/kzltin001/qe/'
    hex_fhgfs = '/researchdata/fhgfs/aifmrm_shared/qe-financial-spillover/'
    local_dir = 'C:\Users\jrr\Documents\GitHub\qe-financial-spillover\data\Objects'
    # this will be used in lines near 224, 288, 292

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



    var_original = [v for v in var]
    var_t1 = [v for v in var]

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
        jump_counter = {a:0 for a in var_original}
        no_jump_counter = {a:0 for a in var_original}
        test_sign= {a:0 for a in var_original}

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
                fund.exp.default_rates = fundamental_default_rates



                fund.var.ewma_delta_prices, \
                fund.var.ewma_delta_fx, \
                fund.exp.prices, \
                fund.exp.exchange_rates = price_fx_expectations(fund, portfolios, currencies, environment)

                fund.exp.exchange_rates, fund.exp.exchange_rate_anchor = anchored_FX_expectations(fund, environment, fx_shock)

                fund.exp.returns = return_expectations(fund, portfolios, currencies, environment)

                # compute the weights of optimal balance sheet positions
                fund.var.weights  = portfolio_optimization_KT(fund,day, tau)


                # intermediate cash position resulting from interest payments, payouts, maturing and defaulting assets
                fund.var.currency_inventory = cash_inventory(fund, portfolios, currencies)

                # compute demand for balance sheet positions
                fund.var.asset_demand, fund.var.currency_demand = asset_demand(fund, portfolios, currencies, environment)



            for ex in exogeneous_agents:
                exogeneous_agents[ex].var.asset_demand = ex_agent_asset_demand(ex, exogeneous_agents, portfolios )



            # Update prices if convergence has not been achieved yet
            if intraday_over == False:
                pre_prices = {}
                for a in portfolios:
                    pre_prices.update({a: a.var.price})


                funds, environment, portfolios, Deltas_h = update_RA_and_fx(portfolios, environment,currencies, funds,exogeneous_agents, var, var_original)

            try:
                Deltas = {v: Deltas_h[v] for v in var_original}
            except:
                print(Deltas_h)

            conv_bound = environment.par.global_parameters['conv_bound']
            convergence,  convergence_condition = check_convergence_cal(Deltas, conv_bound,  tau)


            jump_counter, no_jump_counter, test_sign, environment = I_intensity_parameter_adjustment_cal(
                jump_counter, no_jump_counter, test_sign, Deltas, environment, portfolios, funds, var_t1)

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


            # check for convergece of asset and fx market








            #print ("day:",day,"tau:",tau, convergence, Deltas)

            #calculating and printing degree(in percent) to which the convergence bound is reached. Values <= zero need to be achieved
            list_DeltasA=[abs(Deltas[v]) for v in var_original]
            mean_DA = np.mean(np.array(list_DeltasA))
            max_DA =  np.max(np.array(list_DeltasA))
            FX_DA = abs(np.array(Deltas['FX']))
            print ("day:", day, "tau:", tau, "mean_A:", mean_DA, 'max_A:', max_DA, 'FX:', FX_DA)
            print("deltas",{d: Deltas[d] for d in Deltas})
            print("asset_intensities",{a:a.par.cal_change_intensity for a in portfolios})
            print("fund_intensities",{f: f.par.cal_change_intensity for f in funds})
            #print([a.par.nominal_interest_rate for a in portfolios])

            if tau > 2000:
                print('Calibration convergence failed on day ', day)
                file_name = saving_params["path"] + '/!objects_nonConv_seed_' + str(seed) + '_day_' + str(day) + '.pkl'
                save_objects = open(file_name, 'wb')
                list_of_objects = [portfolios, currencies, environment, exogeneous_agents, funds, seed]
                pickle.dump(list_of_objects, save_objects)
                save_objects.close()


        ##########################################################################################################################
        ############################################## BALANCE SHEET ADJUSTMENT ##################################################
        ###########################################################################################################################

        # updating the covariance matrices
        for fund in funds:
            fund.var.ewma_returns, fund.var.covariance_matrix, fund.var.hypothetical_returns = covariance_estimate(fund,
                                                                                                                   environment,
                                                                                                                   previous_local_currency_returns[
                                                                                                                       fund],
                                                                                                                   inflation_shock)

            # computing new asset and cash positions
        excess_demand, pi, nu = asset_excess_demand_and_correction_factors(funds, portfolios, currencies,
                                                                           exogeneous_agents)

        # trading
        for fund in funds:
            fund.var.assets = fund_asset_adjustments(fund, portfolios, excess_demand, pi, nu)
            fund.var.currency_inventory = fund_cash_inventory_adjustment(fund, portfolios, currencies)
            temp, fund.var.currency_demand = asset_demand(fund, portfolios, currencies, environment)

        for ex in exogeneous_agents:
            exogeneous_agents[ex].var.assets = ex_asset_adjustments(ex, portfolios, excess_demand, pi, nu,
                                                                    exogeneous_agents)

        for fund in funds:
            fund.var.currency_demand = cash_demand_correction(fund, currencies, environment)

        nuC, piC, excess_demandC = cash_excess_demand_and_correction_factors(funds, currencies, exogeneous_agents)

        for fund in funds:
            fund.var.currency = fund_cash_adjustments(nuC, piC, excess_demandC, currencies, fund)

        exogeneous_agents["fx_interventionist"].var.currency = fx_interventionist_cash_adjustment(
            exogeneous_agents["fx_interventionist"], nuC, piC, excess_demandC, currencies)

        # update previous variables
        for fund in funds:
            fund.var_previous = copy_agent_variables(fund.var)

        for portfolio in portfolios:
            portfolio.var_previous = copy.copy(portfolio.var)

        environment.var_previous = copy_env_variables(environment.var)

        exogeneous_agents['central_bank_domestic'].var_previous = copy_cb_variables(
            exogeneous_agents['central_bank_domestic'].var)
        exogeneous_agents['underwriter'].var_previous = copy_underwriter_variables(exogeneous_agents['underwriter'].var)

        # saving objects
        if day>=saving_params["time"]:
            file_name = saving_params["path"] + '/objects_day_' + str(day) + "_seed_" + str(seed) + "_" + obj_label + '.pkl'
            save_objects = open(file_name, 'wb')
            list_of_objects = [portfolios, currencies, environment, exogeneous_agents, funds, seed, obj_label]
            pickle.dump(list_of_objects, save_objects)
            save_objects.close()
    data_t = 0
    return portfolios, currencies, environment, exogeneous_agents, funds,  data_t