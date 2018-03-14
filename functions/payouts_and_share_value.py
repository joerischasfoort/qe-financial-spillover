def calculate_current_value_of_shares(fund, fx_matrix):
    """
    Calculate total value of all assets to determine the value of shares
    :param fund: Fund object for which the value of shares is to be calculated
    :param fx_matrix: pandas DataFrame containing current exchange rates
    :return: float total value of all shares
    """
    value_of_shares = 0
    for asset in fund.var.assets:
        value_of_shares += fund.var.assets[asset] * asset.var.price * fx_matrix.loc[fund.par.country][asset.par.country]
    for currency in fund.var.currency:
        value_of_shares += fund.var.currency[currency] * fx_matrix.loc[fund.par.country][currency.par.country]

    return value_of_shares


def payout_to_shareholders(fund):
    """
    Calculate the amount a fund wants to payout to shareholders
    :param fund: object Fund for which the payout is calculated
    :return: float the value of redeemable shares
    """
    # obtain previous share value
    previous_shares_value = fund.var_previous.redeemable_shares
    # calculate current share target
    shares_target_value = previous_shares_value * (1 + fund.par.target_growth)
    # obtain realised profits
    profits = fund.var.total_profits
    # calculate wanted shares value
    wanted_shares_value = wanted_value_shares(shares_target_value, previous_shares_value, profits)
    current_shares_value = fund.var.redeemable_shares
    # calculate current value of redeemable shares
    payouts = payout(current_shares_value, wanted_shares_value)
    redeemable_shares = current_shares_value - payouts
    return redeemable_shares


def wanted_value_shares(shares_target_value, previous_shares_value, profits):
    """
    Equation 1.4 the wanted share value for a fund
    :param shares_target_value: float target value of shares
    :param previous_shares_value: float previous actual value of shares
    :param profits: float this periods profits
    :return: float the desired level of shares
    """
    wanted_shares_value = min(shares_target_value, previous_shares_value + profits)
    return wanted_shares_value


def payout(shares_value, wanted_shares_value):
    """
    Given the wanted shares value the fund pays out, or asks share holders to commit extra funds
    :param shares_value: float current value of shares
    :param wanted_shares_value: float the desired value of shares
    :return: float payout to shareholders, when negative this amounts to a bail-in by shareholders
    """
    payout = shares_value - wanted_shares_value
    return payout


