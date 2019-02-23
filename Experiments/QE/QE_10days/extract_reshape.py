
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


path2='/Users/Tina/git_repos/qe-financial-spillover/Experiments/QE/QE_10days/results'

#This code is magic - wide to long
df1 = pd.read_csv('prices_long_10days.csv')  
df = df1.iloc[:, 2:]


print df.columns.values

df = df.pivot_table(columns=['asset'], index=['QE', 'seed', 'time'], values='val')
df.to_csv('prices_long_format.csv')
# l = []
# for i in range(50,2500, 100):
# 	l.append(i)
# print len(l)
# print l 

# #Sampling
# path1='/Users/Tina/Dropbox/International Spillovers/Data/results/'
# path2='/Users/Tina/git_repos/qe-financial-spillover/data/'

# #df=pd.read_csv('returns_ls.csv')
# df=pd.read_csv(path2+'summary_largesample.csv') 
# df1=df.sample(frac=0.1, replace=True, random_state=1)
# df1.to_csv(path2+'resample_state1_01.csv')

# df2 = df.iloc[0::100,:]

# df2.to_csv('resample.csv')
###LATEX
# df = pd.read_excel('/Users/Tina/Dropbox/International Spillovers/Data/results/prices.xlsx')  
# df.replace(np.nan, '', inplace=True)

# df = pd.read_csv('dom_bonds.csv')  

# df = df.pivot_table(columns=['time'])
# print df.head()
# df.to_latex('test.tex')