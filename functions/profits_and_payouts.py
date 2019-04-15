from __future__ import division


def profit_and_payout(fund, portfolios, currencies, environment):
    profit_per_asset = {}
    profit_barEx = {}
    payouts = {}
    total_payouts = {c: 0 for c in currencies}
    total_payouts_fx_corr = {}
    total_profit = 0
    for a in portfolios:

        out = a.par.maturity * (1 - a.var.default_rate)
        mat = (1 - a.par.maturity) * (1 - a.var.default_rate)
        all = out + mat

        repayment_effect = mat * (
                    environment.var.fx_rates.loc[fund.par.country, a.par.country] * a.par.face_value / a.par.quantity -
                    environment.var_previous.fx_rates.loc[fund.par.country, a.par.country] * a.var_previous.price)
        rep_effect_barEx = mat * (a.par.face_value / a.par.quantity - a.var_previous.price)  # used to compute payouts

        price_effect = out * (environment.var.fx_rates.loc[fund.par.country, a.par.country] * a.var.price -
                              environment.var_previous.fx_rates.loc[
                                  fund.par.country, a.par.country] * a.var_previous.price)

        p_effect_barEx = out * ( a.var.price - a.var_previous.price)

        interest_effect = all * environment.var.fx_rates.loc[fund.par.country, a.par.country] * (
                    a.par.face_value / a.par.quantity) * a.par.nominal_interest_rate
        int_effect_barEx = all * (
                    a.par.face_value / a.par.quantity) * a.par.nominal_interest_rate  # used to compute payouts

        default_effect = a.var.default_rate * environment.var_previous.fx_rates.loc[
            fund.par.country, a.par.country] * a.var_previous.price
        def_effect_barEx = a.var.default_rate * a.var_previous.price  # used to compute payouts

        profit_per_asset[a] = repayment_effect + price_effect + interest_effect - default_effect

        total_profit = (total_profit + profit_per_asset[a] * fund.var.assets[a])

        payouts[a] = fund.var.assets[a] * (rep_effect_barEx + int_effect_barEx - def_effect_barEx)

        profit_barEx[a] = (rep_effect_barEx + p_effect_barEx +int_effect_barEx - def_effect_barEx)

        for c in currencies:
            if a.par.country == c.par.country:
                total_payouts[c] = total_payouts[c] + payouts[a]

    losses = {}
    for c in currencies:
        profit_per_asset[c] = c.par.nominal_interest_rate * environment.var.fx_rates.loc[fund.par.country, c.par.country] + environment.var.fx_rates.loc[fund.par.country, c.par.country] - environment.var_previous.fx_rates.loc[fund.par.country, c.par.country]
        profit_barEx[c] =  c.par.nominal_interest_rate

        total_payouts[c] = (total_payouts[c] + fund.var.currency[c] * c.par.nominal_interest_rate)
        losses[c] = min(0,total_payouts[c]+fund.var_previous.losses[c])
        total_payouts[c] = max(total_payouts[c]+fund.var_previous.losses[c],0)



        # the balance sheet effect takes into account the exchange rate effects
        total_payouts_fx_corr[c] = total_payouts[c] * environment.var.fx_rates.loc[fund.par.country, c.par.country]

        total_profit = total_profit + profit_per_asset[c] * fund.var.currency[c]

    redeemable_shares = fund.var_previous.redeemable_shares + total_profit - sum(total_payouts_fx_corr.values())

    return profit_per_asset, profit_barEx, losses, redeemable_shares, total_payouts


def profit_and_payout_oc(fund, portfolios, currencies, day):
    """
    Calculate the profits for a fund and what part of those profits it will pay out to shareholders.
    :param fund: fund Object for which profit is to be calculated
    :param portfolios: list of portfolio objects
    :param currencies: list of currency objects
    :return: dictionary of profits per asset, dictionary of losses per currency,
    float redeemable shares size, float total payouts to shareholders
    """
    profit_per_asset = {}
    payouts = {}
    total_payouts = {c: 0 for c in currencies}
    total_profit = 0
    for a in portfolios:
        out = a.par.maturity * (1 - a.var.default_rate[day])
        mat = (1 - a.par.maturity) * (1 - a.var.default_rate[day])
        all = out + mat

        repayment_effect = mat * (a.par.face_value / a.par.quantity - a.var.price[day - 1])
        price_effect = out * (a.var.price[day] - a.var.price[day - 1])
        interest_effect = all * (a.par.face_value / a.par.quantity) * a.par.nominal_interest_rate
        default_effect = a.var.default_rate[day] * a.var.price[day - 1]

        profit_per_asset[a] = repayment_effect + price_effect + interest_effect - default_effect
        total_profit = (total_profit + profit_per_asset[a] * fund.var.assets[a][day-1])
        payouts[a] = fund.var.assets[a][day-1] * (repayment_effect + interest_effect - default_effect)

        for c in currencies:
            # add the profits to the profits to be payed out in the home currency
            total_payouts[c] = total_payouts[c] + payouts[a] # TODO check if this still works with multiple assets

    losses = {}
    for c in currencies:
        profit_per_asset[c] = c.par.nominal_interest_rate
        total_payouts[c] = (total_payouts[c] + fund.var.currency[c][day-1] * c.par.nominal_interest_rate)
        losses[c] = min(0, total_payouts[c] + fund.var.losses[c][day-1])
        total_payouts[c] = max(total_payouts[c] + fund.var.losses[c][day-1], 0)
        total_profit = total_profit + profit_per_asset[c] * fund.var.currency[c][day-1]

    redeemable_shares = fund.var.redeemable_shares[day-1] + total_profit

    return profit_per_asset, losses, redeemable_shares, total_payouts
