import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf

df2 = pd.read_csv(
    '/Users/Tina/Dropbox/International Spillovers/Data/results/timeseries/relative-timeseries-longformat.csv')

#print np.unique(df2['time'])
rows = []
for time in range(0, 998):
    print time
    dict = {}
    df = df2[df2['time'] == time]
    df['dom_bond_yields'] = df['funds[0].exp.returns[portfolios[0]]'] * 100 * 250 * 100
    Y = df['dom_bond_yields']

    X = df['QE']
    X = sm.add_constant(X)
    ols = sm.OLS(Y, X).fit()
    #print (ols.conf_int_el(1)) # qe
    dict[time]=(ols.conf_int_el(1), ols.params[1]) # qe

    rows.append(dict)
print rows

temp=pd.DataFrame(rows)




#temp.to_csv('dom_bond_yields.csv')