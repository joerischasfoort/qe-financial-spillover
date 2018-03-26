from __future__ import division


def profit_and_payout(fund, portfolios, currencies, environment):
    profit_per_asset = {}
    payouts = {}
    total_payouts = {c: 0 for c in currencies}
    total_payouts_fx_corr = {}
    testing = 0
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

        interest_effect = all * environment.var.fx_rates.loc[fund.par.country, a.par.country] * (
                    a.par.face_value / a.par.quantity) * a.par.nominal_interest_rate
        int_effect_barEx = all * (
                    a.par.face_value / a.par.quantity) * a.par.nominal_interest_rate  # used to compute payouts

        default_effect = a.var.default_rate * environment.var_previous.fx_rates.loc[
            fund.par.country, a.par.country] * a.var_previous.price
        def_effect_barEx = a.var.default_rate * a.var_previous.price  # used to compute payouts

        profit_per_asset[a] = repayment_effect + price_effect + interest_effect - default_effect

        total_profit = total_profit + profit_per_asset[a] * fund.var.assets[a]

        payouts[a] = fund.var.assets[a] * (rep_effect_barEx + int_effect_barEx - def_effect_barEx)

        for c in currencies:
            if a.par.country == c.par.country:
                total_payouts[c] = total_payouts[c] + payouts[a]

    for c in currencies:
        profit_per_asset[c] = c.par.nominal_interest_rate * environment.var.fx_rates.loc[
            fund.par.country, c.par.country] + environment.var.fx_rates.loc[fund.par.country, c.par.country] - \
                              environment.var_previous.fx_rates.loc[fund.par.country, c.par.country]

        total_payouts[c] = (total_payouts[c] + fund.var.currency[c] * c.par.nominal_interest_rate)

        # the balance sheet effect takes into account the exchange rate effect
        total_payouts_fx_corr[c] = total_payouts[c] * environment.var.fx_rates.loc[fund.par.country, c.par.country]

        # total_payouts[c]=0

        total_profit = total_profit + profit_per_asset[c] * fund.var.currency[c]

    # print "profit effect:", fund, total_profit

    redeemable_shares = fund.var_previous.redeemable_shares + total_profit - sum(total_payouts_fx_corr.values())

    return profit_per_asset, redeemable_shares, total_payouts