"""Simulation file used to run the model"""
import time
from spillover_model_calRA import *
from spillover_model import *
from calibration_functions import *
import pandas as pd
from stochasticprocess import *
import matplotlib.pyplot as plt
from scipy.optimize import minimize


def opt_fun(x, D_data):

    TS_default_events = ornstein_uhlenbeck_levels(len(D_data)*250, np.mean(D_data)/float(250), x[0]/float(np.mean(D_data)),
                                                  x[1], 1)



    TS_defaults = [np.random.poisson(TS_default_events[idx]) for idx in range(len(TS_default_events))]

    years = range(200)
    D = []
    for t in years:
        D.append(sum(TS_defaults[t*250:t*250 + 250]))

    cor= np.corrcoef(D[1:],D[0:-1])
    cor_data = np.corrcoef(D_data[1:], D_data[0:-1])
    sigma = np.std(D)
    sigma_data = np.std(D_data)

    return ((cor[0,1]-cor_data[0,1])/cor_data[0,1])**2+((sigma-sigma_data)/sigma_data)**2





def plot_defaults(D_data, res):

    TS_default_events = ornstein_uhlenbeck_levels(len(D_data) * 250, np.mean(D_data) / float(250),
                                                      res.x[0] / float(np.mean(D_data)),
                                                      res.x[1], 1)

    TS_defaults = [np.random.poisson(TS_default_events[idx]) for idx in range(len(TS_default_events))]

    years = range(200)
    D = []
    for t in years:
        D.append(sum(TS_defaults[t * 250:t * 250 + 250]))

    cor = np.corrcoef(D[1:], D[0:-1])
    cor_data = np.corrcoef(D_data[1:], D_data[0:-1])
    sigma = np.std(D)
    sigma_data = np.std(D_data)
    print("corelation:", [cor[0,1], cor_data[0,1]])
    print("std:", [sigma, sigma_data])
    plt.plot(D_data[0:100])
    plt.plot(D[0:100])


D_data_ROW = np.array([35,20,23,56,109,136,229,226,119,56,40,30,24,127,268,83,53,83,81,60]*10)*(100/float(120))
D_data_EZ = np.array([35,20,23,56,109,136,229,226,119,56,40,30,24,127,268,83,53,83,81,60]*10)*(20/float(120))


res_ROW = minimize(opt_fun, [4,0.001], args=D_data_ROW, method='nelder-mead')
res_EZ = minimize(opt_fun, [0.5,0.001], args=D_data_EZ, method='nelder-mead')

plot_defaults(D_data_ROW,res_ROW)
plot_defaults(D_data_EZ,res_EZ)