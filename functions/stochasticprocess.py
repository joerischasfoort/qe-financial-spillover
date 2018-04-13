import math
import numpy as np
import random


def exogenous_defaults(environment, portfolios):
    average_yearly_default_events = {}
    daily_default_events = {}
    default_rates_per_default_event = {}
    default_rates = {}
    fundamental_default_rate_expectation = {}

    time = environment.par.global_parameters['end_day']
    avg_y_default_events = environment.par.global_parameters["avg_yearly_default_events"]
    std_y_default_events = environment.par.global_parameters["avg_yearly_default_events_std"]
    mean_reversion_default_events = environment.par.global_parameters["avg_yearly_default_events_mean_reversion"]

    for  i, a in enumerate(portfolios):
        # making one asset riskier than the other
        avg_y_default_events = avg_y_default_events * (i+1)

        average_yearly_default_events[a] = ornstein_uhlenbeck_levels(time, avg_y_default_events,std_y_default_events,mean_reversion_default_events)
        daily_default_events[a] = [np.random.poisson(np.divide(average_yearly_default_events[a][idx], float(250))) for idx
                                   in range(len(average_yearly_default_events[a]))]
        default_rates_per_default_event[a] = np.random.lognormal(environment.par.global_parameters["default_rate_mu"],
                                                                 environment.par.global_parameters["default_rate_std"],
                                                                 len(daily_default_events[a]))
        default_rates[a] = [default_rates_per_default_event[a][idx] * daily_default_events[a][idx] for idx in
                            range(len(default_rates_per_default_event[a]))]
        fundamental_default_rate_expectation[a] = [(average_yearly_default_events[a][idx] / float(250)) * np.exp(
            environment.par.global_parameters["default_rate_mu"]) for idx in range(len(default_rates[a]))]

    return default_rates, fundamental_default_rate_expectation

def ornstein_uhlenbeck_levels(time, init_level, sigma, mean_reversion): # Todo: why are values for parameters hard coded?
    """
    This function returns news about the as a mean-reverting ornstein uhlenbeck process.
    :param init_level: starting point of the default probability
    :param time: total time over which the simulation takes place
    :param rate_of_time: e.g. daily, monthly, annually (default is daily)
    :param sigma: volatility of the stochastic processes
    :param mean_reversion: tendency to revert to the long run average
    :param long_run_average_level:
    :return: list : simulatated default probability simulated over time
    """
    default_events = [init_level]
    for t in range(1, time):

        error = np.random.normal(0, sigma)
        new_dr = (default_events[-1]*(1+error) + mean_reversion * (init_level - default_events[-1]))
        new_dr = max(1e-10,new_dr)
        new_dr = min(500, new_dr)
        default_events.append(new_dr)

    return default_events


