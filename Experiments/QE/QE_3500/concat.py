
import  pickle
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

sys.path.append('/scratch/kzltin001/qe-financial-spillover')

local_dir = "/scratch/kzltin001/qe-financial-spillover/Experiments/QE/QE_3500/Med_3500/"



 
#df_assets = pd.read_csv(local_dir+'df_assets.csv') 
df_prices= pd.read_pickle(local_dir+'df_prices.pickle')
df_exp_returns = pd.read_pickle(local_dir+'df_exp_returns.pickle')

df_list = [ df_prices, df_exp_returns ] 

# df_list = [ df_prices, df_exp_returns ] 

df_final = pd.concat(df_list, keys=['prices', 'returns'])  # concat seeds

print df_final.head()

df_final = df_final.iloc[:, 0:]


print df_final.columns.values 
print df_final.head()
df_final = df_final.pivot_table(columns=['asset'], index=['QE', 'seed', 'time'], values='val')

df_final.to_csv('df_final.csv')

 
