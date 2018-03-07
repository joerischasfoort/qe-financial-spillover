from math import log
from math import exp, expm1
import numpy as np
from functions.weights import *


def update_expectations():
    """
    Method to update expected asset attributes for the next iteration
    1) New expected default probability Equation 1.6
    2) New expected prices, exchange rates Equation 1.7
    3) New expected returns Equation 1.1
    4) Get realised returns for covariance variance matrix  Equation 1.3
    5) Compute new ewma (Mhat) for realised returns   Equation 1.5
    6) Use latest realised
    return and ewma mhat for covariance   Equation 1.4
    5) Calculate new ewma covariance Equation 1.3 continued
    6) Plug it into portfolio optimisation Equation 1.7
    7) get weights...phew!"""

    pass


def exp_return_asset(asset, fund, rho, m, face_value, exp_omega, exp_price, actual_price, quantity):
    """ # TODO
    Method to calculate the expected returns of assets which go into portfolio optimisation Equation 1.5 - 1.6
    :param asset:
    :param fund:
    :param rho: nominal interest rate of asset
    :param m: maturity
    :param face_value: face_value
    :param exp_omega: expected default probability of the underlying asset
    :param exp_price: expected price
    :param actual_price: current price
    :param quantity: global quantity of the asset
    :return: float expected return of the asset
    """
    exp_return = (1 - exp_omega) * (
            ((expected_x * face_value) / (actual_x * actual_price * quantity)) * (rho + 1 - m) + (
            (m * expected_x * exp_price / (actual_x * actual_price)) - 1) - exp_omega)
    return exp_return


def exp_return_cash(): #TODO equation 1.7
    pass


def compute_covar(x, previous_ewma_x, y, previous_ewma_y, previous_covar_ewma, memory_parameter): #TODO equation 1.8
    """compute covar between x and y"""
    covar1 = (x - compute_ewma(x, previous_ewma_x, memory_parameter)) * (y - compute_ewma(y, previous_ewma_y, memory_parameter))
    covar2 = compute_ewma(covar1 , previous_covar_ewma, memory_parameter)
    return covar2


def compute_ewma(variable, previous_ewma, memory_parameter):
    """
    For a fund, calculate expected weighted moving average, equation 1.9
    :param variable: float variable of interest
    :param previous_ewma: float previous exponentially weighted moving average
    :param memory_parameter: float the
    :return: estimate of the exponentially weighted moving average of the variable
    """
    ewma = (1 - memory_parameter) * previous_ewma + memory_parameter * variable
    return ewma


def exp_default_rate(fund, asset, delta_news, std_noise): #TODO equation 1.10
    """
    For a fund, calculate the expected default rate of a certain asset
    :param fund: Fund object which formes the expectation
    :param asset: Asset object about which the expectation is formed
    :param delta_news: float change in the news process about the asset
    :param std_noise: float standard deviation of the agent uncertainty about the news process
    :return: float of the expected default rate
    """
    previously_exp_dr = fund.exp.default_rates[asset]
    default_rate = asset.var.default_rate
    noise = np.random.normal(0, std_noise)
    log_exp_default_rate = log(previously_exp_dr) + delta_news + noise + fund.par.adaptive_param * (log(default_rate) - log(previously_exp_dr))
    exp_default_rate = exp(log_exp_default_rate)
    return exp_default_rate


def exp_price_or_fx(): # TODO equation 1.11
    pass


def exp_price(mhat, phi, last_price):
    """
    The new expected price is the old price times a growth factor. The growth factor is the
    exponentially weighted moving average of past prices with a memory parameter
    :param mhat: last exponentially weighted moving average
    :param phi_p: Memory parameter. If phi_p is 1, only the last observation is considered
    :return:
    """
    exp_price_var = exp_weighted_moving_average( mhat, phi, last_price )  *  last_price  #Calls function from weights.py   Equation 1.6
    return exp_price_var


def exp_return_home_asset( ident,  rho, m, face_value, exp_omega, exp_price, actual_price, global_quantity):
    """
    Method to calculate the expected returns of home assets which go into portfolio optimisation
    Equation 1.2

    :param ident: asset identifier
    :param rho: nominal interest rate of asset
    :param m: constant repayment parameter
    :param face_value:  face_value
    :param exp_omega: expected default probability of the underlying asset (different for every fund)
    :param exp_price: expected price (different for every fund)
    :param actual_price: current price
    :param global_quantity: global quantity of the asset
    :return:
    """
    # Exclude cash
    if not "cash" in ident:
         # Returns of the asset = returns from interest payment, returns from price changes, returns from principal payment
        var = (1 - exp_omega )  * (    (face_value/(actual_price * global_quantity)) * (rho + 1 -m) +    (  (m * exp_price / actual_price)  -1 )    -  exp_omega   )
        return var
    # if it's cash, expected return is 0
    else:
        return 0.0


def exp_return_abroad_asset(ident, fund_region, rho, m, face_value, exp_omega, exp_price, actual_price, global_quantity, actual_x_rate, expected_x_rate):
    "We need the actual and expected exchange rate "

    # We exclude cash; not pretty but ok
    if not "cash" in ident:
        #We need to be careful if the fund_region is "home" or "abroad". According to the region,
        # the exchange rate has to be taken as direct quote or indirect quote

        #So we first take the "domestic" fund guys and DIRECT exchange rate quotation:
        if "domestic" in fund_region:
            # Assign the actual and expected direct xrate quotation
            expected_x = expected_x_rate["x_domestic_to_foreign"]
            actual_x = actual_x_rate["x_domestic_to_foreign"][-1]

            var = (1 - exp_omega) * ((  (expected_x * face_value) / ( actual_x  * actual_price * global_quantity)) * (rho + 1 - m) + ((m * expected_x *  exp_price / (actual_x *actual_price) ) - 1) - exp_omega)
            return var

        # Now the  "foreign" fund guys which need INDIRECT  exchange rate quotation:
        if "foreign" in fund_region:
            # Assign the actual and expected indirect xrate quotation
            expected_x = 1/ expected_x_rate["x_domestic_to_foreign"]
            actual_x = 1/ actual_x_rate["x_domestic_to_foreign"][-1]

            var = (1 - exp_omega) * (
                    ((expected_x * face_value) / (actual_x * actual_price * global_quantity)) * (rho + 1 - m) + (
                        (m * expected_x * exp_price / (actual_x * actual_price)) - 1) - exp_omega)

            return var
    # if it's cash, expected return is 0 (easy)
    else:
        return 0.0

