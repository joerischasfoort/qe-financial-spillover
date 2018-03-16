from math import log
from math import exp
import numpy as np


def price_adjustment(portfolios, environment, exogeneous_agents , funds, a):
    """
    Find the next  price.
  
    """     
    #Equation 1.18 : Get aggregate demand over all funds and exogenous agents
    total_demand = {i:0 for i in portfolios}
    
    
    total_demand_exogenous_agents = {i:0 for i in portfolios}
    #first loop over all exogenous agents and collect their demand per asset
    
    for ex in exogeneous_agents:
         
        total_demand_exogenous_agents[a] += exogeneous_agents[ex].var.asset_demand[a]

    # collect total demand from agents per asset
    for fund in funds:
        total_demand[a] += fund.var.asset_demand[a]
    
    #exit the fund loop and take into account underwriter and central bank demand
    total_demand[a] = total_demand[a] + total_demand_exogenous_agents[a]
   
    #Equation 1.17 : price adjustment 
    log_new_price  = log(a.var.price) +  environment.par.global_parameters['p_change_intensity'] *  total_demand[a]/a.par.quantity    
    return exp(log_new_price)

    
def fx_adjustment(portfolios, currencies, environment, exogeneous_agents , funds):
    """
    Find the new fxrate
  
    """
    
    # We iterate over the  exchange rate matrix to get all 
    # possible combinations of "from_country" "to_country"
    # then calculate the new exchange rate for every exchange rate pair above the diagonal 
    
    # Make a list of combinations
    combinations = []
    
    for column in range(len(environment.var.fx_rates.index)):
        row=0
     
    while row<column:
        combination_tuple = (environment.var.fx_rates.index[row], environment.var.fx_rates.columns[column])
        row =row + 1
        combinations.append(combination_tuple)
        
        
    fx_demand = 0 # respective exchange demand
    fx_rate =  0 # respective exchange demand
    
    
    for el in combinations:
         
        weight_df = 0 # This is the sum of   weights per fund DEMANDING a currency (the first sum in equation 1.22)
        aux = 0 #helper variable 
        
        weight_fd = 0 # This is the sum of   weights per fund from the other perspective (the second term in the nominator term inequation 1.22 )
        aux_2 = 0 # helper variable
        
        for fund in funds:
            #we look for all demand of the "from" country, e.g. the first element of the tuple in the list of combinations
            if fund.par.country == el[0]: 
                for weight in fund.var.weights:
                # Then we look for all weights that are outside of the fund's own country
                    if fund.par.country != weight.par.country:  
 
                        weight_df += fund.var.weights[weight]
                        
                aux = (fund.var.redeemable_shares/environment.var.fx_rates[el[0]][el[1]]) * weight_df
            
            #then look for all supply of the "to" country, e.g. the second element of the tuple in the list of combinations
            
            if fund.par.country == el[1]: 
 
                for weight in fund.var.weights:
                     if fund.par.country !=  weight.par.country:  
                         weight_fd += fund.var.weights[weight]
                aux_2 = (fund.var.redeemable_shares) * weight_fd
        
        if aux + aux_2!=0:
            fx_demand = np.divide(aux - aux_2, aux + aux_2)
        else:
            fx_demand = 0
        
        #Generate noise
        market_noise = np.random.normal(0, 0.1)  # We get the random noise 
    
        log_new_fx_rate = log(environment.var.fx_rates[el[0]][el[1]]) + environment.par.global_parameters["fx_change_intensity"] * fx_demand + market_noise
        fx_rate = exp(log_new_fx_rate)
            
        environment.var.fx_rates[el[0]][el[1]] =  fx_rate
        environment.var.fx_rates[el[1]][el[0]] =  1/ fx_rate
        
    return environment.var.fx_rates
    
     