"""Calculate realised returns for assets"""
import numpy as np


def realised_returns(omega, V, P, P_tau, Q, rho, m, X=1):
    """
    Calculate realised returns for domestic or foreign asset equations (1.6-1.7)
    :param omega: default probability
    :param V: Face value
    :param P: Last price
    :param P_tau: Market maker price
    :param Q: Asset quantity
    :param rho: interest rate
    :param m: maturity
    :param X: float exchange rate calculated as X^{FD}= 1 / X^{DF}, standard no exchange rate X = 1
    :return: float realised return
    """
    realised_return = (1 - omega) * (np.divide(X * V, X* P * Q) * (rho + 1 - m) + np.divide(X* m * P_tau, X * P) - 1) - omega
    return realised_return
