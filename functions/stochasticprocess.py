import math
import numpy as np
import random

def ornstein_uhlenbeck_levels(time=500, init_level=10e-7, sigma=0.125, mean_reversion=0.99):
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

    #np.random.seed(2) #remeber to take out
    default_probability = [init_level]
     
    for t in range(1, 100000):

        error = np.random.normal(0, sigma)
        new_dr = default_probability[-1] + mean_reversion * (init_level - default_probability[-1]) + error
        new_dr = max(0,new_dr)
        default_probability.append(new_dr)

    return default_probability
