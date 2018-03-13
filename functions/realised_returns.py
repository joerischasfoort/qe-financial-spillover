"""Calculate realised returns for assets"""
import numpy as np


def hypothetical_asset_returns(fund, prices_tau, fx_rates):
    """Calculate hypothetical returns on asset portfolio"""
    realised_rets = {}
    realised_profits = {}
    for asset in fund.var.assets:
        realised_profits[asset] = realised_profits_asset(asset.var.default_rate,
                                                      asset.par.face_value,
                                                      asset.var.price,
                                                      prices_tau[asset],
                                                      fund.var.assets[asset],
                                                      asset.par.nominal_interest_rate,
                                                      asset.par.maturity,
                                                      fx_rates.loc[fund.par.country][asset.par.country])
        realised_rets[asset] = realised_returns_asset(realised_profits[asset], prices_tau[asset],
                                                      fx_rates.loc[fund.par.country][asset.par.country])
    total_realised_profits = sum(realised_profits.values())
    return realised_rets, total_realised_profits


def realised_returns_asset(realised_profit, price, exchange_rate=1):
    """
    Equation 1.5 Calculate realised return on an asset
    :param realised_profit: float realised profit on asset
    :param price: float current asset price
    :param exchange_rate: float current exchange rate (1 for domestic)
    :return: float realised return on the asset
    """
    return realised_profit / (exchange_rate * price)


def realised_return_cash(realised_profit, exchange_rate=1):
    """
    Calculate realised return on cash
    :param realised_profit: float realised profit on currency
    :param exchange_rate: float current exchange rate (1 for domestic)
    :return: float realised return on cash
    """
    return realised_profit / exchange_rate


def realised_profits_asset(default_rate, face_value, previous_price, price, quantity,
                           interest_rate, maturity, previous_exchange_rate=1, exchange_rate=1):
    """
    Equation 1.1 - 1.2 Calculate realised returns for domestic or foreign asset
    :param default_rate: float default rate
    :param face_value: float Face value
    :param previous_price: float Last price
    :param price: float current price
    :param quantity: float total asset quantity
    :param interest_rate: float nominal interest rate
    :param maturity: float maturity
    :param previous_exchange_rate: float exchange rate calculated as previous_exchange_rate^{FD}= 1 / previous_exchange_rate^{DF}, standard no exchange rate previous_exchange_rate = 1
    :param exchange_rate: float new exchange rate
    :return: float realised return on asset
    """
    out = maturity * (1 - default_rate)
    mat = (1 - maturity) * (1 - default_rate)
    all = out + mat
    repayment_effect = mat * (previous_exchange_rate * np.divide(face_value, float(quantity)) - previous_exchange_rate * previous_price)
    price_effect = out * (exchange_rate * price - previous_exchange_rate * previous_price)
    interest_effect = all * exchange_rate * np.divide(face_value, float(quantity)) * interest_rate
    default_effect = default_rate * previous_exchange_rate * previous_price
    realised_profit = repayment_effect + price_effect + interest_effect - default_effect
    return realised_profit


def realised_profits_cash(interest_rate, previous_exchange_rate=1, exchange_rate=1):
    """
    Equations 1.3 Calculate realised returns on currency, if home currency, exchange rates are 1 and realised profits
    are equal to the interest rate.
    :param interest_rate: float nominal interest rate on currency
    :param previous_exchange_rate: float previous exchange rate
    :param exchange_rate: float current exchange rate
    :return: float realised profit on one unit of currency
    """
    realised_profit = exchange_rate * interest_rate + exchange_rate - previous_exchange_rate
    return realised_profit
