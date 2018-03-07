from math import log
from math import exp
import numpy as np


def price_adjustment(portfolios, currencies, environment, exogeneous_agents , funds):
    """
    Find the next  price.
  
    """
 
    #Equation 1.19 : Get aggregate demand 
    total_demand = {}
    
    # collect total demand from agents per asset
    for a in portfolios:
        for fund in funds:
            total_demand[a] +=  fund.var.asset_demand[a]
        
        #exit the fund loop and take into account underwriter and central bank demand
        
        total_demand[a] = total_demand[a] + exogenous_agents["underwriter"] + exogenous_agents["central_bank_domestic"]
        
  
    #Equation 1.20 : price adjustment 
    for a in portfolios:
        log_new_price  = log(a.var.price) +  environment.par.p_change_intensity *  total_demand[a]/a.par.quantity
        a.var.price = exp(log_new_price)
        
        
    
    #Now exchange rates
    market_noise = np.random.normal(0, 0.1)  # We get the random noise 
    
    #Calculate demand
    
    total_fx_demand = 0.0
    
    # get demand for environment.var.fx_rates.loc["domestic", "foreign" ]
    
    
    # We need to operate on the exchange rate panda
    
    for fund in funds: 
        
        for key in fund.var.weights:
            
            if fund.var.weights[key].country != fund.par.country
    
    # Eventually adjust price 
    
    # Convention change environment.var.fx_rates.loc["domestic", "foreign" ] : X^DF
    
    log_new_fx =  log(environment.var.fx_rates.loc["domestic", "foreign" ]  ) + environment.par.fx_change_intensity *  total_fx_demand  + market_noise 
    
    environment.var.fx_rates.loc[0,1] =  exp(log_new_fx)
    
    # Take the inverse
    environment.var.fx_rates.iloc[1,0] =  1: exp(log_new_fx)
    
     
    
 