
import  pickle
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


#This code is magic
df1 = pd.read_csv('returns_largesample.csv')
df = df1.iloc[:, 2:]


print df.columns.values
df = df[(df['QE']!=0) &(df['time']<1000)]

df = df.pivot_table(columns=['asset'], index=['QE', 'seed', 'time'], values='val')
df.to_csv('returns_ls.csv')
