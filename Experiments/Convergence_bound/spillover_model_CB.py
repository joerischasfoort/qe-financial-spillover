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


def spillover_model_CB(portfolios, currencies, environment, exogeneous_agents, funds,  seed, obj_label):

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
    data = initdatadict(funds, portfolios, currencies, environment, deltas ) # create tau data dictionary
    data_t = copy.deepcopy(data) # create t data dictionary
    ######################################################################
    ##### Determine directoring for saving objects and measurement########
    ######################################################################
    hex_home = '/home/jriedler/qe-financial-spillover/Experiments/Convergence_bound/Objects_CB/'
    hex_fhgfs = '/researchdata/fhgfs/aifmrm_shared/qe-financial-spillover/'
    local_dir = 'Objects_CB/'
    # this will be used in lines near 224, 288, 292
    ######################################################################
    #######################################################################




    ##################################################################################
    ###################### COMPUTING STOCHASTIC PROCESSES ############################
    ##################################################################################
    # calculating stochastic components default
    days = environment.par.global_parameters["end_day"]
    default_rates, fundamental_default_rate_expectation, shock_processes = stochastic_timeseries(environment.par.global_parameters, portfolios,days,seed)

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

        # these two variables are needed for the pricing algorithm
        var = copy.copy(portfolios)
        var_t1 = []

        for row in environment.var.fx_rates.index:
            for col in environment.var.fx_rates.columns:
                environment.var.ewma_fx_rates.loc[row, col] = compute_ewma(environment.var.fx_rates.loc[row, col], environment.var.ewma_fx_rates.loc[row, col],0.01)


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
        #fx_shock = 0

        inflation_shock = {}
        for key in todays_shocks:
            if key.split("_")[1] == "inflation":
                inflation_shock[key] = todays_shocks[key]

        # calculate expected default rates
        previous_return_exp = {} #TODO: This should be done when passing all other values to "var_previous

        for fund in funds:
            fund.exp.default_rates = dr_expectations(fund, portfolios, delta_news, fundamental_default_rates, default_expectation_noise[fund])
            previous_return_exp[fund]=fund.exp.returns.copy() # TODO: This should be done when passing all other values to "var_previous
        ###################################################################################################
        ###################################################################################################


        ###########################################################
        ############# RESETTING INTRADAY PARAMETERS ###############
        ###########################################################
        convergence=False
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
        ###########################################################
        ###########################################################


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
                environment, Delta_Demand, Delta_Capital = shock_FX(portfolios, environment, exogeneous_agents, funds, currencies, fx_shock)

            #############################################################################
            #############################################################################

            for fund in funds:
                # shareholder dividends and fund profits 
                fund.var.profits, \
                fund.var.losses, \
                fund.var.redeemable_shares, \
                fund.var.payouts = profit_and_payout(fund, portfolios, currencies, environment)

                # Expectation formation
                fund.var.ewma_delta_prices, \
                fund.var.ewma_delta_fx, \
                fund.exp.prices, \
                fund.exp.exchange_rates = price_fx_expectations(fund, portfolios, currencies, environment)

                fund.exp.exchange_rates = anchored_FX_expectations(fund, environment)

                fund.exp.returns = return_expectations(fund, portfolios, currencies, environment)


                # compute the weights of optimal balance sheet positions
                fund.var.weights, ow, u, ix  = portfolio_optimization(fund)


                # intermediate cash position resulting from interest payments, payouts, maturing and defaulting assets
                fund.var.currency_inventory = cash_inventory(fund, portfolios, currencies)

                # compute demand for balance sheet positions
                fund.var.asset_demand, fund.var.currency_demand = asset_demand(fund, portfolios, currencies, environment)

            for ex in exogeneous_agents:
                exogeneous_agents[ex].var.asset_demand = ex_agent_asset_demand(ex, exogeneous_agents, portfolios )




            if intraday_over == False:
                Delta_Demand = {}
                Delta_Capital = {}

                for a in portfolios:
                    if a in var:
                        a.var.price, Delta_str, delta_demand = price_adjustment(portfolios, environment,
                                                                                exogeneous_agents, funds, a,
                                                                                a.par.change_intensity)  # TODO: is the Delta_str really necessary?
                        Delta_Demand.update({a: delta_demand})
                    else:
                        a.var.price, Delta_str, delta_demand = price_adjustment(portfolios, environment,
                                                                                exogeneous_agents, funds, a,
                                                                                0)  # TODO: is the Delta_str really necessary?
                        Delta_Demand.update({a: delta_demand})

                    environment.var.fx_rates, Delta_Capital = fx_adjustment(portfolios, currencies, environment, funds,
                                                                            0)

                if "FX" in var:
                    environment.var.fx_rates, Delta_Capital = fx_adjustment(portfolios, currencies, environment, funds,
                                                                            environment.par.global_parameters[
                                                                                "fx_change_intensity"])





            Deltas = {}
            Deltas.update(Delta_Demand)
            Deltas.update({"FX": Delta_Capital})

            convergence_bound = {}
            convergence_bound.update({a: environment.par.global_parameters["convergence_bound"] for a in portfolios})
            convergence_bound.update({"FX": environment.par.global_parameters["convergence_bound"] })

            convergence_condition = {i: abs(Deltas[i]) < convergence_bound[i] for i in Deltas}
            asset_market_convergence = sum([convergence_condition[a] for a in portfolios])
            convergence = sum(convergence_condition[i] for i in convergence_condition) == len(Deltas) and tau > 1
            if tau > 10001: convergence = True # exit iteration after many iterations

            # jumps only count when they are caused by a change in the price or fx
            jump_counter, no_jump_counter, test_sign, environment = I_intensity_parameter_adjustment(
                    jump_counter, no_jump_counter, test_sign, Deltas, environment, convergence_bound,var_t1)

            var_t1 = var

            if asset_market_convergence == len(portfolios) and len(var)<= len(portfolios):
                var.append("FX")


            #print ("day:",day,"tau:",tau, tau%3, convergence, Deltas)


            #Update intraday data points
            #data = update_data(data, funds, portfolios, currencies, environment, Deltas)
            #this is where intraday simulation ends

            # saving objects when there is no convergence (for diagnostic purpose)
            if tau > 10000:
                dir = local_dir
                file_name = local_dir + '!noCONV_objects_day_' + str(day) + "_seed_" + str(seed) + "_" + obj_label +  '.pkl'
                save_objects = open(file_name, 'wb')
                list_of_objects = [portfolios, currencies, environment, exogeneous_agents, funds, seed]
                pickle.dump(list_of_objects, save_objects)
                save_objects.close()

        #pd.DataFrame(data).to_csv( local_dir  + 'data' + '/' + "intraday" + "/" + "intraday_data_day_" + str(day) + ".csv")


        ##########################################################################################################################
        ############################################## BALANCE SHEET ADJUSTMENT ##################################################
        ###########################################################################################################################

        # updating the covariance matrices
        for fund in funds:
            fund.var.ewma_returns, fund.var.covariance_matrix, fund.var.hypothetical_returns = covariance_estimate(fund,  environment, previous_return_exp[fund], inflation_shock)

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
        #show_fund(funds[0], portfolios, currencies, environment)
        #show_fund(funds[1], portfolios, currencies, environment)

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
        #pd.DataFrame(data_t).to_csv( local_dir + 'data/' + "data_t.csv")

        # saving objects
        #if day>=environment.par.global_parameters["end_day"]-1000 or (day-1) % 250 == 0:
        if day >= 0:
            file_name = local_dir + 'objects_day_' + str(day) + "_seed_" + str(seed) + "_" + obj_label + '.pkl'
            save_objects = open(file_name, 'wb')
            list_of_objects = [portfolios, currencies, environment, exogeneous_agents, funds, seed, obj_label]
            pickle.dump(list_of_objects, save_objects)
            save_objects.close()

    return portfolios, currencies, environment, exogeneous_agents, funds,  data_t