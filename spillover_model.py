"""Main model"""
import numpy as np
import random
import copy
import pandas as pd
from functions.payouts_and_share_value import *
from functions.port_opt import *
from functions.asset_demands import *
from functions.ex_agent_asset_demands import *
from functions.balance_sheet_adjustments import *
from functions.stochasticprocess import *
from functions.expectation_formation import *
from functions.market_mechanism import *
from functions.profits_and_payouts import *
from functions.show import *
#from functions.realised_returns import *
from functions.supercopy import *


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
    # create tau data dictionary
    data = {str(a) + 'price': [environment.par.global_parameters["init_asset_price"]] for a in portfolios}

    news_process = ornstein_uhlenbeck_levels(environment.par.global_parameters["days"],
                                             environment.par.global_parameters["default_rate_mu"],
                                             environment.par.global_parameters["default_rate_std"],
                                             environment.par.global_parameters["default_rate_mean_reversion"])
    # We get the random noise 
    fx_shock = [ np.random.normal(0, environment.par.global_parameters["fx_shock_std"]) for i in range(environment.par.global_parameters["days"]) ] 
    
    for a in portfolios:
        a.var.aux_ret = convert_P2R(a,a.var.price)
        if a.var.aux_ret<=0:
            a.var.aux_ret=0.0001

    for day in range(1, environment.par.global_parameters["days"]):
        # initialise intraday prices at current price
        prices_tau = {portfolio: portfolio.var.price for portfolio in portfolios}
        delta_news = news_process[day] - news_process[day-1]

        # determine value and payouts to shareholders
        for fund in funds:
            fund.exp.default_rates = dr_expectations(fund, portfolios, delta_news)

        show_fund(funds[0], portfolios, currencies, environment)
        show_fund(funds[1], portfolios, currencies, environment)



        convergence=False
        intraday_over=False

        for tau in range(10000): #TODO this needs to be rewritten into a while loop when stopping criteria are defined


#            if tau == 1000:
#                environment.par.global_parameters["p_change_intensity"]=0.01
#            if tau == 3000:
#                environment.par.global_parameters["p_change_intensity"]=0.001
#            if tau == 5000:
#                environment.par.global_parameters["p_change_intensity"]=0.0001
            if convergence == True:
                intraday_over = True

            for fund in funds:
                # shareholder dividends and fund profits 
                fund.var.profits, \
                fund.var.redeemable_shares, \
                fund.var.payouts = profit_and_payout(fund, portfolios, currencies, environment)
                

                
                
                
                
                # 1 Expectation formation
                fund.var.ewma_delta_prices, \
                fund.var.ewma_delta_fx, \
                fund.exp.prices, \
                fund.exp.exchange_rates = price_fx_expectations(fund, portfolios, currencies, environment)
                fund.exp.returns = return_expectations(fund, portfolios, currencies, environment)
                fund.var.ewma_returns, fund.var.covariance_matrix = covariance_estimate(fund, portfolios)

                #print fund, fund.exp.returns

                # compute the weights of optimal balance sheet positions
                fund.var.weights = portfolio_optimization(fund)
                
                # intermediate cash position resulting from interest payments, payouts, maturing and defaulting assets
                fund.var.currency_inventory = cash_inventory(fund, portfolios, currencies)
                #print fund, fund.var.currency_inventory[currencies[0]],  fund.var_previous.currency[currencies[0]] + fund.var.assets[portfolios[0]]*((1-portfolios[0].var.default_rate)*(1-portfolios[0].par.maturity)+portfolios[0].var.default_rate)*portfolios[0].var.price
                
                # compute demand for balance sheet positions
                fund.var.asset_demand, fund.var.currency_demand = asset_demand(fund, portfolios, currencies, environment)
                
                
                
                c0_t = fund.var_previous.currency[currencies[0]]
                c1_t = fund.var_previous.currency[currencies[1]]
                rhoC0 = currencies[0].par.nominal_interest_rate
                rhoC1 = currencies[1].par.nominal_interest_rate
                rho0 = portfolios[0].par.nominal_interest_rate
                rho1 = portfolios[1].par.nominal_interest_rate
                Q0_t = fund.var_previous.assets[portfolios[0]]
                Q1_t = fund.var_previous.assets[portfolios[1]]
                fxC0_t1 = environment.var.fx_rates.loc[fund.par.country][currencies[0].par.country]
                fxC1_t1 = environment.var.fx_rates.loc[fund.par.country][currencies[1].par.country]
                fxC0_t = environment.var_previous.fx_rates.loc[fund.par.country][currencies[0].par.country]
                fxC1_t = environment.var_previous.fx_rates.loc[fund.par.country][currencies[1].par.country]
                fx0_t1 = environment.var.fx_rates.loc[fund.par.country][portfolios[0].par.country]
                fx1_t1 = environment.var.fx_rates.loc[fund.par.country][portfolios[1].par.country]
                fx0_t = environment.var_previous.fx_rates.loc[fund.par.country][portfolios[0].par.country]
                fx1_t = environment.var_previous.fx_rates.loc[fund.par.country][portfolios[1].par.country]
                p0_t1 = portfolios[0].var.price
                p1_t1 = portfolios[1].var.price
                p0_t = portfolios[0].var_previous.price
                p1_t = portfolios[1].var_previous.price
                
                dC0 = fxC0_t1*(c0_t*(1+rhoC0)+rho0*Q0_t)-c0_t*fxC0_t
                dC1 = fxC1_t1*(c1_t*(1+rhoC1)+rho1*Q1_t)-c1_t*fxC1_t

                d0 = Q0_t*(fx0_t1*p0_t1-fx0_t*p0_t)
                d1 = Q1_t*(fx1_t1*p1_t1-fx1_t*p1_t)
                
                
                
                newA = Q0_t*p0_t1*fx0_t1+Q1_t*p1_t1*fx1_t1
                newC = fund.var.currency_inventory[currencies[0]]*fxC0_t1 + fund.var.currency_inventory[currencies[1]]*fxC1_t1

                #print "asset side effect:", fund, newA+newC-fund.var.redeemable_shares

            
            for ex in exogeneous_agents:
                exogeneous_agents[ex].var.asset_demand = ex_agent_asset_demand(ex, exogeneous_agents, portfolios )


            if intraday_over == False:            
                for a in portfolios:
                    a.var.price, a.var.aux_ret = price_adjustment(portfolios, environment, exogeneous_agents, funds, a)

                environment.var.fx_rates = fx_adjustment(portfolios, currencies, environment, exogeneous_agents , funds, fx_shock[day]) 


            if tau == 9998:
                convergence=True

            for a in portfolios:
                data[str(a) + 'price'].append(a.var.price) #TODO remove when done
        
            
            
            #this is where intraday calculations end
        

        
        #computing new asset and cash positions

        excess_demand, pi, nu = asset_excess_demand_and_correction_factors(funds, portfolios, currencies, exogeneous_agents)


         # trading
        for fund in funds:
            fund.var.assets = fund_asset_adjustments(fund, portfolios, excess_demand, pi, nu)
            fund.var.currency_inventory = fund_cash_inventory_adjustment(fund, portfolios, currencies)

        for ex in exogeneous_agents:
            exogeneous_agents[ex].var.assets = ex_asset_adjustments(ex, portfolios, excess_demand, pi, nu, exogeneous_agents)
    
        # balance sheet adjustment
        for fund in funds:
            fund.var.currency_demand = cash_demand_correction(fund, currencies,environment)
        
        nuC, piC, excess_demandC = cash_excess_demand_and_correction_factors(funds, portfolios, currencies, exogeneous_agents)


        for fund in funds:
            fund.var.currency = fund_cash_adjustments(nuC, piC, excess_demandC, currencies, fund, environment)
            
        show_fund(funds[0], portfolios, currencies, environment)
        show_fund(funds[1], portfolios, currencies, environment)


        # update previous variables
        for fund in funds:
            fund.var_previous = copy_agent_variables(fund.var)

        for portfolio in portfolios:
            portfolio.var_previous = copy.copy(portfolio.var)

        exogeneous_agents['central_bank_domestic'].var_previous = copy_cb_variables(exogeneous_agents['central_bank_domestic'].var)
        exogeneous_agents['underwriter'].var_previous = copy_underwriter_variables(exogeneous_agents['underwriter'].var)

    pd.DataFrame(data).to_csv('intraday_data.csv')

    return portfolios, currencies, environment, exogeneous_agents, funds