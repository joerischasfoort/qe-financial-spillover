def payout_to_shareholders(fund):
    # calculate current share target
    shares_target_value = 1
    # obtain previous share value
    previous_shares_value = 1
    # obtain realised profits
    profits = 1
    # calculate wanted shares value
    wanted_shares_value = wanted_value_shares(shares_target_value, previous_shares_value, profits)
    current_shares_value = 1 # TODO sum of assets + currencies
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


