from math import log
from math import exp
import numpy as np


def price_adjustment(portfolios, currencies, environment, exogeneous_agents , funds):
    """
    Find the next  price.
  
    """
 
    #Equation 1.20 : Get aggregate demand 
    total_demand = {}
    
    # collect total demand from agents per asset
    for a in portfolios:
        for fund in funds:
            total_demand[a] +=  fund.var.asset_demand[a]
        
        #exit the fund loop and take into account underwriter and central bank demand
        total_demand[a] = total_demand[a] + exogenous_agents["underwriter"] + exogenous["central_bank_domestic"]
        
  
    #Equation 1.19 : price adjustment 
    for a in portfolios:
        log_new_price  = log(a.var.price) +  environment.par.p_change_intensity *  total_demand[a]/a.par.quantity
        a.var.price = exp(log_new_price)
        
        
    
    #Now exchange rates!
    
    #Generate noise
    market_noise = np.random.normal(0, 0.1)  # We get the random noise 
    
    
    # We iterate over the  exchange rate matrix to get all 
    # possible combinations of "from_country" "to_country"
    # then calculate the new exchange rate for every exchange rate pair above the diagonal 
    
    
    # Make a list of combinations
    combinations = []
    
    for column in range(len(environment.var.fx_rates.index)):
    row=0
     
    while row<column:
        combination_tuple = (row, column)
        row =row + 1
        combinations.append(combination_tuple)
    
    
    
    fx_demand = 0 # respective exchange demand
    fx_rate =  0 # respective exchange demand
    
    for el in combinations:
        
        
        foreign_weight = 0 # This is the sum of foreign weights per fund DEMANDING a currency (the first sum in equation 1.22)
        aux = 0 #helper variable 
        
        foreign_weight_2 # This is the sum of foreign weights per fund from the other perspective (the second term in the nominator term inequation 1.22 )
        aux_2 = 0 # helper variable
        
        for fund in funds:
            
            #we look for all demand of the "from" country, e.g. the first element of the tuple in the list of combinations
            if fund.par.country == el[0]: 
                

                for weight in fund.var.weights:
                # Then we look for all weights that are outside of the fund's own country
                    if fund.par.country != weight.asset.country:  #ask Joeri or Jesper!!
                        
                        foreign_weight += weight
                        
                aux = (fund.var.redeemable_shares/environment.var.fx_rates[el[0]][el[1]]) * foreign_weight
            
            #then look for all supply of the "to" country, e.g. the second element of the tuple in the list of combinations
            if fund.par.country == el[1]: 
                for weight in fund.var.weights:
                     if fund.par.country != weight.asset.country:  #ask Joeri or Jesper!!
                         foreign_weight_2 += weight
                         
                 aux_2 = (fund.var.redeemable_shares) * weight

                     
        fx_demand = (aux - aux_2)/(aux + aux_2)
        
        
        log_new_fx_rate = log(environment.par.fx_rates[el[0]][el[1]]) +  environment.par.fx_change_intensity *  fx_demand  + market_noise
        fx_rate = exp(log_new_fx_rate)
            
        environment.par.fx_rates[el[0]][el[1]] =  fx_rate
        environment.par.fx_rates[el[1]][el[0]] =  1/ fx_rate
  
    
     
    
 