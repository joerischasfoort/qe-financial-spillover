"""Calculate realised returns for assets"""
import numpy as np






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
    repayment_effect = mat * (exchange_rate * np.divide(face_value, float(quantity)) - previous_exchange_rate * previous_price)
    price_effect = out * (exchange_rate * price - previous_exchange_rate * previous_price)
    interest_effect = all * exchange_rate * np.divide(face_value, float(quantity)) * interest_rate
    default_effect = default_rate * previous_exchange_rate * previous_price
    realised_profit = repayment_effect + price_effect + interest_effect - default_effect
    return realised_profit
