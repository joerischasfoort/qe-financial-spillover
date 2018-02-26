"""Main model"""
import numpy as np
import random

def spillover_model(assets, funds, days, seed):
    """
    Kozai, Riedler & Schasfoort Agent-based simulation model of financial spillovers
    :param assets: list of Asset objects
    :param funds: list of Fund objects
    :param days: integer amount of days over which the simulation will take place
    :param seed: integer used to seed the random number generator
    :return: lists of assets, funds
    """
    random.seed(seed)
    np.random.seed(seed)

    for day in range(days-1):
        tau = 0
        for fund in funds:
            fund.expected_vars = update_expectations(fund, assets, assets.exchange_rate, tau)