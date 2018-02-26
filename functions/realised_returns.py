"""Calculate realised returns for assets"""
import numpy as np


def realised_returns_domestic(omega, V, P, P_tau, Q, rho, m):
    """
    Calculate realised returns for domestic asset equation 1.6
    :param omega: default probability
    :param V: Face value
    :param P: Last price
    :param P_tau: Market maker price
    :param Q: Asset quantity
    :param rho: interest rate
    :param m: maturity
    :return: float realised return
    """
    realised_return = (1 - omega) * (np.divide(V, P * Q) * (rho + 1 -m) + np.divide(m * P_tau, P) -1) - omega
    return realised_return