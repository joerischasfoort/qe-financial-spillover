import numpy as np
import matplotlib.pyplot as plt
import random
from functions.market_mechanism import *





def stochastic_timeseries(parameters,portfolios,days,seed):
    shock_processes = correlated_shocks(parameters,days,seed)

    default_rates = {}
    fundamental_default_rate_expectation = {}

    for a in portfolios:
        default_rates[a], fundamental_default_rate_expectation[a] =exogenous_defaults(parameters, a,days,seed)

    return default_rates, fundamental_default_rate_expectation, shock_processes





def correlated_shocks(parameters, days,seed):

    risk_components = ["domestic_inflation","foreign_inflation","fx_shock"]

    corrs=np.zeros((len(risk_components),len(risk_components)))
    stds=corrs.copy()
    means = np.zeros((len(risk_components)))
    for i, rc in enumerate(risk_components):
        means[i]=parameters[rc + "_mean"]
        stds[i,i]=parameters[rc + "_std"]
        for i2, rc2 in enumerate(risk_components):
            var=rc + "_and_" + rc2
            if rc==rc2:
                corrs[i, i2] = 1
            if var in parameters["list_risk_corr"].keys():
                corrs[i,i2]= parameters["list_risk_corr"][var]

    covs = np.dot(np.dot(stds,corrs),stds)
    random.seed(seed+10)
    np.random.seed(seed+10)
    m = np.random.multivariate_normal(means, covs, days).T
    shock_processes = {rc: m[i] for i, rc in enumerate(risk_components)}

    return shock_processes






def exogenous_defaults(parameters, a,days,seed):

    time = days
    default_events_mean_reversion = parameters["default_events_mean_reversion"]


    default_events_mean = parameters[a.par.country + "_default_events_mean"]
    default_events_std =  parameters[a.par.country + "_default_events_std"]
    default_rate_mean = parameters[a.par.country + "_default_rate_mean"]
    default_rate_std = parameters[a.par.country + "_default_rate_std"]

    TS_default_events = ornstein_uhlenbeck_levels(time, default_events_mean,default_events_std,default_events_mean_reversion,seed)

    random.seed(seed+1)
    np.random.seed(seed+1)
    TS_defaults = [np.random.poisson(TS_default_events[idx]) for idx in range(len(TS_default_events))]


    TS_default_rate_per_event = np.random.normal(default_rate_mean, default_rate_std,len(TS_default_events))

    TS_default_rates = [TS_default_rate_per_event[idx] * TS_defaults[idx] for idx in range(len(TS_default_events))]

    TS_true_default_rate_expectation = [TS_default_events[idx] * default_rate_mean for idx in range(len(TS_default_events))]

    return TS_default_rates, TS_true_default_rate_expectation





def ornstein_uhlenbeck_levels(time, init_level, sigma, mean_reversion,seed): # Todo: why are values for parameters hard coded?

    default_events = [init_level]
    random.seed(seed+2)
    np.random.seed(seed+2)
    for t in range(1, time):
        error = np.random.normal(0, sigma)
        new_dr = (default_events[-1]*(1+error) + mean_reversion * (init_level - default_events[-1]))
        new_dr = max(1e-10,new_dr)
        new_dr = min(500, new_dr)
        default_events.append(new_dr)

    return default_events


def shock_FX(portfolios, environment, exogeneous_agents, funds, currencies, shock):
    # shocking prices and exchange rates
    Delta_Demand = {}
    lastP = {a: a.par.change_intensity for a in portfolios}
    lastFX = environment.par.global_parameters['fx_change_intensity']
    for a in portfolios:
        a.par.change_intensity = 0
    environment.par.global_parameters['fx_change_intensity'] = 0

    for a in portfolios:
        a.var.price, Delta_str, delta_demand = price_adjustment(portfolios, environment,
                                                                               exogeneous_agents, funds,
                                                                               a)
        Delta_Demand.update({a: delta_demand})

    environment.var.fx_rates.iloc[0, 1] = environment.var.fx_rates.iloc[0, 1] * (1 + shock)
    environment.var.fx_rates.iloc[1, 0] = 1 / environment.var.fx_rates.iloc[0, 1]
    environment.var.fx_rates, Delta_Capital = fx_adjustment(portfolios, currencies, environment, funds)

    for a in portfolios:
        a.par.change_intensity = lastP[a]

    environment.par.global_parameters['fx_change_intensity'] = lastFX

    return environment, Delta_Demand, Delta_Capital