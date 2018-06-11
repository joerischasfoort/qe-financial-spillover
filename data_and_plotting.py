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
cov_01 = []
fx = []
ewma_fx =[]
tau = []
p1 = []
p0 = []
r0 = []
r1 = []


for day in range(1,200):
    filename = "data/Objects/objects_day_" + str(day) + "_seed_1"  + "_benchHE"+".pkl"
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

    cov_11.append(funds[1].var.covariance_matrix.loc[currencies[1],currencies[1]])
    cov_00.append(funds[0].var.covariance_matrix.loc[currencies[0], currencies[0]])
    cov_01.append(funds[1].var.covariance_matrix.loc[portfolios[0], portfolios[1]])


    fx.append(environment.var.fx_rates.iloc[0,1])

    ewma_fx.append(1/environment.var.ewma_fx_rates.iloc[0,1])

    p1.append(portfolios[1].var.price)
    p0.append(portfolios[0].var.price)
    r1.append(funds[1].exp.returns[portfolios[1]])
    r0.append(funds[1].exp.returns[portfolios[0]])



