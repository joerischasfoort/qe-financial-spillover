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
import time
from init_objects import *



list_of_risk_correlation = {}
list_of_risk_correlation.update({'domestic_inflation'+"_and_" +'foreign_inflation': 0.0})
list_of_risk_correlation.update({'foreign_inflation'+"_and_" +'domestic_inflation': list_of_risk_correlation['domestic_inflation'+"_and_" +'foreign_inflation']})
list_of_risk_correlation.update({'domestic_inflation'+"_and_" +'fx_shock': -0.0})
#list_of_risk_correlation.update({'foreign_inflation'+"_and_" +'domestic_fx_shock': -0.17})


# 1 setup parameters
parameters = { #Todo: cleaning and spell checking!!
    # global parameters
    "n_domestic_assets": 1,
    "n_foreign_assets": 1,
    "n_domestic_funds": 1,
    "n_foreign_funds": 1,
    "list_risk_corr": list_of_risk_correlation,
    "domestic_price_index": 1,
    "foreign_price_index": 1,
    "domestic_inflation_mean": 0.0,
    "foreign_inflation_mean": 0.0,
    "domestic_inflation_std": 0.02/float(250),
    "foreign_inflation_std": 0.02/float(250),
    "start_day": 1,
    "end_day": 5,
    "p_change_intensity": 0.0001,
    "fx_change_intensity": 0.0001,
    "cov_memory": 0.00,
    # asset parameters
    "face_value": 5000,
    "nominal_interest_rate": 0.02/250,
    "currency_rate": 0.0/250,
    "maturity" : 0.99988093,
    "quantity" : 5000,
    # agent parameters
    "price_memory": 0.0,
    "fx_memory": 0.0,
    "fx_reversion_speed": 0.15/250,
    "local_currency_return_weight": 1,
    "risk_aversion": 5.0,
    "domestic_risk_aversion_D_asset": 5,
    "domestic_risk_aversion_F_asset": 5,
    "foreign_risk_aversion_D_asset": 5,
    "foreign_risk_aversion_F_asset": 5,
    "news_evaluation_error": 0,
    # cb parameters
    "cb_country": 'domestic',
    # initial values
    "init_asset_price": 1.0,
    "init_exchange_rate": 1.0,
    "total_money": 1000,
    "init_agent_ewma_delta_prices": 1,
    "init_ewma_delta_fx": 1,
    "init_asset_demand": 0,
    "init_currency_demand": 0,
    "init_payouts": 0,
    "init_losses": 0,
    "init_profits": 0,
    # shock processes parameters
    "fx_shock_mean": 0.0,
    "fx_shock_std": 0.0,
    "domestic_default_events_mean": 80 / float(250),
    "foreign_default_events_mean": 80 / float(250),
    "domestic_default_events_std": 10 / float(250),
    "foreign_default_events_std": 10 / float(250),
    "default_events_mean_reversion": 1,# 0.001,
    "domestic_default_rate_mean": 0.02 / float(80),
    "foreign_default_rate_mean": 0.02 / float(80),
    "domestic_default_rate_std": 0,
    "foreign_default_rate_std": 0,
    "default_rate_mean_reversion": 1,
    "default_rate_delta_t": 0.003968253968253968,
    'conv_bound': 0.01,
    "adaptive_param": 0.0  # For expected default rate
}



obj_label = "sym_4_assets"
seed = 1

saving_params = {}
#saving_params.update({"path": 'C:\Users\jrr\Documents\GitHub\qe-financial-spillover\data\Objects'})
saving_params.update({"path": 'data/Objects'})
saving_params.update({"time": 0})


# 2 initalise model objects
portfolios, currencies, funds, environment, exogenous_agents = init_objects(parameters, seed)


variable = [0.99988093, 0.9994602]
i = 0
for a in portfolios:
    if a.par.country =="domestic":
        a.par.maturity = variable[i]
        i = i + 1
        if i == len(variable) :
            i = 0
    if a.par.country =="foreign":
        a.par.maturity = variable[i]
        i = i + 1
        if i == len(variable) :
            i = 0

variable = [5000, 2500]
for a in portfolios:
    if a.par.country =="domestic":
        a.par.quantity = variable[1]
        a.par.face_value = a.par.quantity = variable[1]
    if a.par.country == "foreign":
        a.par.quantity = variable[0]
        a.par.face_value = a.par.quantity = variable[0]


@profile
def spillover_model(portfolios, currencies, environment, exogeneous_agents, funds,  seed, obj_label,saving_params):
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

                fund.exp.local_currency_returns, fund.exp.cons_returns, fund.exp.returns = return_expectations(fund, portfolios, currencies, environment)

                # compute the weights of optimal balance sheet positions
                #fund.var.weights  = portfolio_optimization(fund)
                fund.var.weights = portfolio_optimization_KT(fund,day, tau)
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


            #print ("day:",day,"tau:",tau, convergence, Deltas)

            #calculating and printing degree(in percent) to which the convergence bound is reached. Values <= zero need to be achieved
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
        if day>=saving_params["time"]:
            file_name = saving_params["path"] + '/objects_day_' + str(day) + "_seed_" + str(seed) + "_" + obj_label + '.pkl'
            save_objects = open(file_name, 'wb')
            list_of_objects = [portfolios, currencies, environment, exogeneous_agents, funds, seed, obj_label]
            pickle.dump(list_of_objects, save_objects)
            save_objects.close()

    return portfolios, currencies, environment, exogeneous_agents, funds,  data_t


# 3 simulate model
start = time.time()
portfolios, currencies, environment, exogenous_agents, funds, data_t = spillover_model(portfolios, currencies, environment, exogenous_agents, funds, seed, obj_label, saving_params)
end = time.time()
#print(i, end - start)
