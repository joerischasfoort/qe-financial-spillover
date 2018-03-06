from math import log
from math import exp
import numpy as np


def price_adjustment(funds, portfolios, exogenous_agents, p_change_intensity):
    """
    Find the next  price.
  
    """
 
    #Equation 1.19 : Get aggregate demand 
    total_demand = {}
    
      # collect total demand from agents per asset
      for a in portfolios:
          for fund in funds: 
          
              total_demand[a] +=  fund.var.asset_demand[a] 
          #exit the loop and take into account underwriter demand
          total_demand[a] = total_demand[a] + exogenous_agents.underwriter[a]

    #Equation 1.20 : price adjustment 
    for a in portfolios:
        log_new_price  = log(asset.var.price[a]) +  p_change_intensity *  total_demand[a]/asset.par.quantity[a]
        asset.var.price[a] = exp(log_new_price)
    
    #Now exchange rates
    # We get the random noise 
     
    market_noise = np.random.normal(0, 0.1) 
     
        
      # collect total demand from agents per asset
      for a in portfolios:
          for fund in funds: 
          
              total_demand[a] +=  fund.var.asset_demand[a] 
          #exit the loop and take into account underwriter demand
          total_demand[a] = total_demand[a] + exogenous_agents.underwriter[a]
         
    log_new_xrate  = log(asset.var.price[a]) +  p_change_intensity *  total_demand[a]/asset.par.quantity[a] + market_noise
    asset.var.price[a] = exp(log_new_xrate)        