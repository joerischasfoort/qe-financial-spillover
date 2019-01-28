"""Simulation file used to run the model"""
import time
from spillover_model_calRA import *
from spillover_model import *
from calibration_functions import *
import pandas as pd
from stochasticprocess import *
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import math



df_inflation = pd.read_csv('C:\Users\jrr\Dropbox\International Spillovers\Data\inflation\CPI_96.csv')
df_interest= pd.read_excel('C:\Users\jrr\Dropbox\International Spillovers\Data\interest_rates\deposit_rates.xls',sheet_name='data')
df_penn= pd.read_excel('C:\Users\jrr\Dropbox\International Spillovers\Data\inflation\penworldtable90.xlsx', Sheet_name="Sheet5")
df_penn = df_penn.drop(df_penn[df_penn.year != 2014].index)

ROW_countries = ['Argentina', 'Australia', 'Bermuda', 'Botswana', 'Brazil', 'Canada', 'Chile', 'China', 'Colombia', 'Czech Republic', 'Denmark', 'HongKong', 'Hungary', 'India', 'Indonesia', 'Israel', 'Japan', 'Kuwait', 'Lebanon', 'Liechtenstein', 'Malaysia', 'Mexico', 'Monaco', 'Namibia', 'New Zealand', 'Norway', 'Oman', 'Pakistan', 'Peru', 'Philippines', 'Puerto Rico', 'Poland', 'Russia', 'Singapore', 'South Africa', 'Korea', 'Sweden', 'Switzerland', 'Taiwan', 'Thailand', 'Turkey', 'United Kingdom', 'United States', 'Venezuela', 'Vietnam']


inflation = {df_inflation.iloc[i][0]:df_inflation.iloc[i][20] for i in range(len(df_inflation))}
interest = {df_interest.iloc[i][0]:df_interest.iloc[i][3] for i in range(len(df_interest))}
rgdp = {df_penn.iloc[i][1]: df_penn.iloc[i][5]  for i in range(len(df_penn))}

inf = {}
int = {}
gdp = {}
for i in ROW_countries:
    try:
        if math.isnan(float(inflation[i])) != True:
            try:
                inflation[i]
                interest[i]
                rgdp[i]
                inf.update({i: inflation[i]})
                int.update({i: interest[i]})
                gdp.update({i: rgdp[i]})
            except:
                print(i, "not in all samples")
    except:
        print(i, "not in all samples")

real_rate = {i: float(int[i])-float(inf[i]) for i in int}

sum_gdp = sum(gdp[i] for i in gdp)
weight = {i: gdp[i]/sum_gdp for i in gdp}

weighted_rates = {i: real_rate[i]*weight[i] for i in weight}
result = sum(weighted_rates[i] for i in weighted_rates)

int_weight = {i: float(int[i])*weight[i] for i in weight}
inf_weight = {i: float(inf[i])*weight[i] for i in weight}

res_inf = sum(inf_weight[i] for i in inf_weight)
res_int = sum(int_weight[i] for i in int_weight)


