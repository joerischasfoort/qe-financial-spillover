import numpy as np
import pandas as pd
import random
from functions.market_mechanism import *


def stochastic_timeseries(parameters, portfolios, days, seed):
    shock_processes = correlated_shocks(parameters, days, seed)

    default_rates = {}
    fundamental_default_rate_expectation = {}

    for a in portfolios:
        default_rates[a], fundamental_default_rate_expectation[a] = exogenous_defaults(parameters, a, days, seed)

    return default_rates, fundamental_default_rate_expectation, shock_processes


def stochastic_timeseries_2(parameters,portfolios,start_day, end_day,seed0,seed1):
    shock_processes = correlated_shocks_2(parameters,start_day, end_day,seed0,seed1)

    default_rates = {}
    fundamental_default_rate_expectation = {}

    for a in portfolios:
        default_rates[a], fundamental_default_rate_expectation[a] = exogenous_defaults_2(parameters, a, start_day, end_day, seed0, seed1)

    return default_rates, fundamental_default_rate_expectation, shock_processes


def calculate_covariance_matrix(assets, historical_returns):
    """
    Calculate the covariance matrix of several assets and currencies provided their returns
    :param list of asset objects: portfolio's and currencies
    :param historical_returns: list of lists historical returns for each asset
    :return: DataFrame of the covariance matrix of stocks and money (in practice just the variance).
    """
    covariances = np.cov(np.array([hst_rets for hst_rets in historical_returns]))

    return pd.DataFrame(covariances, index=assets, columns=assets)


def correlated_shocks(parameters, days, seed):

    risk_components = ["domestic_inflation", "foreign_inflation", "fx_shock"]

    corrs = np.zeros((len(risk_components),len(risk_components)))
    stds = corrs.copy()
    means = np.zeros((len(risk_components)))
    for i, rc in enumerate(risk_components):
        means[i]=parameters[rc + "_mean"]
        stds[i, i]=parameters[rc + "_std"]
        for i2, rc2 in enumerate(risk_components):
            var = rc + "_and_" + rc2
            if rc == rc2:
                corrs[i, i2] = 1
            if var in parameters["list_risk_corr"].keys():
                corrs[i, i2]= parameters["list_risk_corr"][var]

    covs = np.dot(np.dot(stds, corrs), stds)

    random.seed(seed+10)
    np.random.seed(seed+10)
    m = np.random.multivariate_normal(means, covs, days).T

    shock_processes = {rc: m[i] for i, rc in enumerate(risk_components)}

    return shock_processes


def correlated_shocks_2(parameters, start_day, end_day,seed0,seed1):

    risk_components = ["domestic_inflation","foreign_inflation","fx_shock"]

    corrs = np.zeros((len(risk_components),len(risk_components)))
    stds = corrs.copy()
    means = np.zeros((len(risk_components)))
    for i, rc in enumerate(risk_components):
        means[i] = parameters[rc + "_mean"]
        stds[i, i]= parameters[rc + "_std"]
        for i2, rc2 in enumerate(risk_components):
            var = rc + "_and_" + rc2
            if rc == rc2:
                corrs[i, i2] = 1
            if var in parameters["list_risk_corr"].keys():
                corrs[i, i2]= parameters["list_risk_corr"][var]

    covs = np.dot(np.dot(stds,corrs),stds)

    random.seed(seed0+10)
    np.random.seed(seed0+10)
    m0 = np.random.multivariate_normal(means, covs, start_day).T
    random.seed(seed1+10)
    np.random.seed(seed1+10)
    m1 = np.random.multivariate_normal(means, covs, end_day).T
    m_h = np.zeros((len(m1[:,0]),len(m1[0,start_day:end_day])))
    for i in range(len(m_h[:,0])):
        for j in range(len(m_h[0,:])):
            m_h[i,j]=m1[i,j+start_day]
    m = np.append(m0,m_h,1)

    shock_processes = {rc: m[i] for i, rc in enumerate(risk_components)}

    return shock_processes


def exogenous_defaults_2(parameters, a, start_day, end_day,seed0,seed1):


    default_events_mean_reversion = parameters["default_events_mean_reversion"]

    try:
        default_events_mean = a.par.mean_default_events
        default_events_std =  a.par.default_events_std
        default_rate_mean =   a.par.default_rate_mean
        default_rate_std =    a.par.default_rate_std
        default_events_mean_reversion = a.par.default_events_mean_reversion

    except AttributeError:
        default_events_mean = parameters[a.par.country + "_default_events_mean"]
        default_events_std = parameters[a.par.country + "_default_events_std"]
        default_rate_mean = parameters[a.par.country + "_default_rate_mean"]
        default_rate_std = parameters[a.par.country + "_default_rate_std"]
        default_events_mean_reversion = parameters["default_events_mean_reversion"]

    #id_num = int(filter(str.isdigit, str(a)))  # give each asset a number in order to avoid correlated default events
    id_num = sum(ord(a.par.country[i]) for i in range(len(a.par.country)))

    TS_default_events = ornstein_uhlenbeck_levels_2(start_day,end_day, default_events_mean,default_events_std,default_events_mean_reversion,seed0 + 1 + id_num,seed1 + 1 + id_num)

    random.seed(seed0 + 2 + id_num)
    np.random.seed(seed0+ 2 + id_num)
    TS_defaults = [np.random.poisson(TS_default_events[idx]) for idx in range(start_day)]

    random.seed(seed1 + 2 + id_num)
    np.random.seed(seed1+ 2 + id_num)
    for idx in range(start_day,end_day):
        TS_defaults.append(np.random.poisson(TS_default_events[idx]))


    random.seed(seed0 + 3 + id_num)
    np.random.seed(seed0+ 3 + id_num)
    TS_default_rate_per_event = np.random.normal(default_rate_mean, default_rate_std,start_day)

    random.seed(seed1 + 3 + id_num)
    np.random.seed(seed1 + 3 + id_num)
    TS_default_rate_per_event = np.append(TS_default_rate_per_event,np.random.normal(default_rate_mean, default_rate_std, end_day-start_day))

    TS_default_rates = [np.array(TS_default_rate_per_event)[idx] * (np.array(TS_defaults)[idx]) for idx in range(len(TS_default_events))]

    TS_true_default_rate_expectation = [TS_default_events[idx] * default_rate_mean for idx in range(len(TS_default_events))]

    return TS_default_rates, TS_true_default_rate_expectation


def exogenous_defaults(parameters, a, days, seed):

    time = days
    default_events_mean_reversion = parameters["default_events_mean_reversion"]

    try:
        default_events_mean = a.par.mean_default_events
        default_events_std = a.par.default_events_std
        default_rate_mean = a.par.default_rate_mean
        default_rate_std = a.par.default_rate_std
        default_events_mean_reversion = a.par.default_events_mean_reversion

    except AttributeError:
        default_events_mean = parameters[a.par.country + "_default_events_mean"]
        default_events_std = parameters[a.par.country + "_default_events_std"]
        default_rate_mean = parameters[a.par.country + "_default_rate_mean"]
        default_rate_std = parameters[a.par.country + "_default_rate_std"]
        default_events_mean_reversion = parameters["default_events_mean_reversion"]

    # id_num = int(filter(str.isdigit, str(a)))  # give each asset a number in order to avoid correlated default events
    id_num = sum(ord(a.par.country[i]) for i in range(len(a.par.country)))

    TS_default_events = ornstein_uhlenbeck_levels(time, default_events_mean, default_events_std,
                                                  default_events_mean_reversion, seed + 1 + id_num)

    random.seed(seed + 2 + id_num)
    np.random.seed(seed + 2 + id_num)
    TS_defaults = [np.random.poisson(TS_default_events[idx]) for idx in range(len(TS_default_events))]

    random.seed(seed + 3 + id_num)
    np.random.seed(seed + 3 + id_num)
    TS_default_rate_per_event = np.random.normal(default_rate_mean, default_rate_std, len(TS_default_events))

    TS_default_rates = [TS_default_rate_per_event[idx] * TS_defaults[idx] for idx in range(len(TS_default_events))]

    TS_true_default_rate_expectation = [TS_default_events[idx] * default_rate_mean for idx in
                                        range(len(TS_default_events))]

    return TS_default_rates, TS_true_default_rate_expectation


def ornstein_uhlenbeck_levels(time, init_level, sigma, mean_reversion,seed): # Todo: why are values for parameters hard coded?

    default_events = [init_level]
    random.seed(seed)
    np.random.seed(seed)
    for t in range(1, time):
        error = np.random.normal(0, sigma)
        new_dr = exp(np.log((default_events[-1])+error + mean_reversion * (np.log(init_level) - np.log(default_events[-1]))))


        default_events.append(new_dr)

    return default_events


def ornstein_uhlenbeck_levels_2(time0, time1, init_level, sigma, mean_reversion,seed0,seed1): # Todo: why are values for parameters hard coded?

    default_events = [init_level]
    random.seed(seed0)
    np.random.seed(seed0)

    for t in range(1, time0):
        error = np.random.normal(0, sigma)
        new_dr = exp(np.log((default_events[-1])+error + mean_reversion * (np.log(init_level) - np.log(default_events[-1]))))
        default_events.append(new_dr)

    random.seed(seed1)
    np.random.seed(seed1)
    for t in range(time0, time1):
        error = np.random.normal(0, sigma)
        new_dr = exp(np.log((default_events[-1])+error + mean_reversion * (np.log(init_level) - np.log(default_events[-1]))))
        default_events.append(new_dr)

    return default_events


def shock_FX(portfolios, environment, exogeneous_agents, funds, currencies, shock):
    # shocking prices and exchange rates
    Delta_Demand = {}
    # adjustment intensities are zero - prices and fx do not adjust
    for a in portfolios:
        a.var.price, Delta_str, delta_demand = price_adjustment(portfolios, environment,
                                                                               exogeneous_agents, funds,
                                                                               a,0)
        Delta_Demand.update({a: delta_demand})

    environment.var.fx_rates.iloc[0, 1] = environment.var.fx_rates.iloc[0, 1] * (1 + shock)
    environment.var.fx_rates.iloc[1, 0] = 1 / environment.var.fx_rates.iloc[0, 1]
    environment.var.fx_rates, Delta_Capital = fx_adjustment(portfolios, currencies, environment, funds,0)

    Deltas = {}
    Deltas.update(Delta_Demand)
    Deltas.update({"FX": Delta_Capital})

    return environment, Deltas
