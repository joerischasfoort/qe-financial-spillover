

def initdatadict(funds, portfolios, currencies, environment):

    data = {str(a) + 'price': [environment.par.global_parameters["init_asset_price"]] for a in portfolios}

    all_assets = portfolios + currencies
    for fund in funds:
        redeem_s = {"redeemable_shares" + "_fund_" + str(fund.name): [fund.var.redeemable_shares]}
        data.update(redeem_s)
        for a in all_assets:
            exp_returns = {"exp_return_" + str(a) + "_fund_" + str(fund.name): [fund.exp.returns[a]] for return_ in fund.exp.returns}
            data.update(exp_returns)
            weights = { "weight_" +str(a) + "_fund_" + str(fund.name):  [fund.var.weights[a]]  for weight in fund.var.weights }
            data.update(weights)

        for a in portfolios:
            exp_df = {"exp_default_" + str(a) + "_fund_" + str(fund.name): [fund.exp.default_rates[a]] for df in fund.exp.default_rates}
            data.update(exp_df)

            a_demands = {"a_demand_" + str(a) + "_fund_" + str(fund.name): [fund.var.asset_demand[a]] for demand in fund.var.asset_demand}
            data.update(a_demands)

        for c in currencies:
            c_demands = {"c_demand_" + str(c) + "_fund_" + str(fund.name): [fund.var.currency_demand[c]] for demand in fund.var.currency_demand}
            data.update(c_demands)


    data["Delta_Capital"] = [0]
    data["FX_rate_domestic_foreign"] = [environment.var.fx_rates.loc["domestic"][ "foreign"]]  #Todo: general case!
    return data


def update_data(data, funds, portfolios, currencies, environment, Delta_Capital):
    all_assets = portfolios + currencies
    for a in portfolios:
        data[str(a) + 'price'].append(a.var.price)  # TODO remove when done

    for fund in funds:
        data["redeemable_shares" + "_fund_" + str(fund.name)].append(fund.var.redeemable_shares)
        for a in portfolios:
            data["exp_default_" + str(a) + "_fund_" + str(fund.name)].append(fund.exp.default_rates[a])
            data["a_demand_" + str(a) + "_fund_" + str(fund.name)].append(fund.var.asset_demand[a])

        for c in currencies:
            data["c_demand_" + str(c) + "_fund_" + str(fund.name)].append(fund.var.currency_demand[c])

        for a in all_assets:
            data["weight_" + str(a) + "_fund_" + str(fund.name)].append(fund.var.weights[a])
            data["exp_return_" + str(a) + "_fund_" + str(fund.name)].append(fund.exp.returns[a])


    data["Delta_Capital"].append(Delta_Capital)
    data["FX_rate_domestic_foreign"].append(environment.var.fx_rates.loc["domestic"]["foreign"]) #Todo: general case!
    return data

def reset_intraday(data):
    for key, value in data.iteritems():
        del value[:-1]
    return data
