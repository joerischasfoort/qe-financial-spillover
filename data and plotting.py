import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv('C:\Users\jrr\Documents\GitHub\qe-financial-spillover\data\intraday\intraday_data_day_1.csv')

x = data.iloc[1,1]


import pickle

data = open('objects.pkl', 'wb')
seed=1
testing = [portfolios, currencies, environment, exogeneous_agents, funds, seed]

pickle.dump(testing,data)

data.close()


