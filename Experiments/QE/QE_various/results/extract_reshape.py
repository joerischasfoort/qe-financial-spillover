
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
#df.to_csv('prices_long_format.csv')