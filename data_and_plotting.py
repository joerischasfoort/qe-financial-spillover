import  pickle
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#variables to extract
domestic_weight_in_foreign_assets=[]
foreign_weight_in_domestic_assets=[]
cov = []
cov_00 = []
cov_11 = []
fx = []
tau = []


for day in range(10000,10300):
    filename = "data/Objects/objects_day_" + str(day) +".pkl"
    data = open(filename,"rb")
    list_of_objects = pickle.load(data)

    portfolios = list_of_objects[0]
    currencies = list_of_objects[1]
    environment = list_of_objects[2]
    exogeneous_agents = list_of_objects[3]
    funds = list_of_objects[4]

    tau.append(environment.var.tau)

    domestic_weight_in_foreign_assets.append(funds[0].var.weights[portfolios[1]]+funds[0].var.weights[currencies[1]])
    foreign_weight_in_domestic_assets.append(funds[1].var.weights[portfolios[0]]+funds[1].var.weights[currencies[0]])
    cov.append(funds[1].var.covariance_matrix.loc[portfolios[1],portfolios[1]]-funds[1].var.covariance_matrix.loc[portfolios[0],portfolios[0]])

    cov_11 = cov_11.append(funds[1].var.covariance_matrix.loc[portfolios[1],portfolios[1]])
    cov_00 = cov_00.append(funds[1].var.covariance_matrix.loc[portfolios[0], portfolios[0]])

    fx.append(1/environment.var.fx_rates.iloc[0,1])


