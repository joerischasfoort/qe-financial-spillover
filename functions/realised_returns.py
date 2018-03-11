"""Calculate realised returns for assets"""
import numpy as np


def hypothetical_asset_returns(fund, prices_tau, fx_rates):
    """Calculate hypothetical returns on asset portfolio"""
    realised_rets = {}
    for asset in fund.var.assets:
        realised_rets[asset] = realised_returns(asset.var.default_rate,
                                                asset.par.face_value,
                                                asset.var.price,
                                                prices_tau[asset],
                                                fund.var.assets[asset],
                                                asset.par.nominal_interest_rate,
                                                asset.par.maturity,
                                                fx_rates.loc[fund.par.country][asset.par.country])


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
