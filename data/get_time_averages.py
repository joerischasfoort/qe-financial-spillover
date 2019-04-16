

import pandas as pd
 
df= pd.read_csv('data_largesample.csv')



var_list_assets = ['funds[3].exp.returns[currencies[0]]', # domestic currency
            'funds[0].exp.returns[currencies[1]]',  # foreign currency
            'funds[0].exp.returns[portfolios[0]]',   # domestic bond
            'funds[0].exp.returns[portfolios[1]]',  #  domestic equity
            'funds[3].exp.returns[portfolios[2]]',   # foreign bond
            'funds[3].exp.returns[portfolios[3]]',  #  foreign equity
                ]

var_list_price = [ 'percentage_portfolio2', 'percentage_portfolio1',
                   'percentage_portfolio0' ,'percentage_fx_rates.iloc[0,1]', 'percentage_portfolio3' ]

lista = var_list_assets +var_list_price 

#dom_bonds = df.groupby(['QE','seed'])['funds[0].exp.returns[portfolios[0]]'].mean()

domestic_assets = df.groupby(['QE','seed'])[lista].mean().reset_index()
 
domestic_assets.to_csv('test.csv')
