"""Calculate realised returns for assets"""
import numpy as np






def realised_profits_asset(default_rate, face_value, previous_price, price, quantity,
                           interest_rate, maturity, previous_exchange_rate, exchange_rate):

    out = maturity * (1 - default_rate)
    mat = (1 - maturity) * (1 - default_rate)
    all = out + mat
    repayment_effect = mat * (exchange_rate * np.divide(face_value, float(quantity)) - previous_exchange_rate * previous_price)
    price_effect = out * (exchange_rate * price - previous_exchange_rate * previous_price)
    interest_effect = all * exchange_rate * np.divide(face_value, float(quantity)) * interest_rate
    default_effect = default_rate * previous_exchange_rate * previous_price
    realised_profit = repayment_effect + price_effect + interest_effect - default_effect
    return realised_profit

def realised_profits_currency(interest_rate, previous_exchange_rate, exchange_rate):
    realized_profit= exchange_rate * interest_rate + exchange_rate - previous_exchange_rate
    return realized_profit