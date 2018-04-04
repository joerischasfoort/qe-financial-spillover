

def initdatadict(funds, portfolios, currencies, environment, deltas):

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

            as = {"a_quantity" + str(a) + "_fund_" + str(fund.name): [fund.var.assets[a]] for a in fund.var.assets}
            data.update(as)


        for a in portfolios:
            exp_df = {"exp_default_" + str(a) + "_fund_" + str(fund.name): [fund.exp.default_rates[a]] for df in fund.exp.default_rates}
            data.update(exp_df)
            exp_df = {"exp_default_" + str(a) + "_fund_" + str(fund.name): [fund.exp.default_rates[a]] for df in fund.exp.default_rates}

            a_demands = {"a_demand_" + str(a) + "_fund_" + str(fund.name): [fund.var.asset_demand[a]] for demand in fund.var.asset_demand}
            data.update(a_demands)

        for c in currencies:
            cs = {"c_quantity" + str(a) + "_fund_" + str(fund.name): [fund.var.currency[c]] for c in fund.var.currency}
            data.update(cs)
            c_demands = {"c_demand_" + str(c) + "_fund_" + str(fund.name): [fund.var.currency_demand[c]] for demand in fund.var.currency_demand}
            data.update(c_demands)



    for i in deltas:
        data[i] = [deltas[i]]

    data["FX_domestic_foreign"] = [environment.var.fx_rates.loc["domestic"][ "foreign"]]  #Todo: general case!

    for fund in funds:
        for idx_x, asset_x in enumerate(fund.var.covariance_matrix.columns):
            for idx_y, asset_y in enumerate(fund.var.covariance_matrix.columns):
                if idx_x <= idx_y:
                    varcovar =  { "var_covar_" +   "fund_" + str(fund.name) + "_" + str(asset_x) + "_"  + str(asset_y): [ fund.var.covariance_matrix.loc[asset_x][asset_y]]}
                    data.update(varcovar)
                    #print idx_x, asset_x, idx_y ,asset_y
    return data


def update_data(data, funds, portfolios, currencies, environment, Deltas):
    all_assets = portfolios + currencies
    for a in portfolios:
        data[str(a) + 'price'].append(a.var.price)  # TODO remove when done

    for fund in funds:
        data["redeemable_shares" + "_fund_" + str(fund.name)].append(fund.var.redeemable_shares)
        for a in portfolios:
            data["exp_default_" + str(a) + "_fund_" + str(fund.name)].append(fund.exp.default_rates[a])
            data["a_demand_" + str(a) + "_fund_" + str(fund.name)].append(fund.var.asset_demand[a])
            data["a_quantity" + str(a) + "_fund_" + str(fund.name)].append(fund.var.assets[a])

        for c in currencies:
            data["c_demand_" + str(c) + "_fund_" + str(fund.name)].append(fund.var.currency_demand[c])
            data["c_quantity" + str(a) + "_fund_" + str(fund.name)].append(fund.var.currency[c])


        for a in all_assets:
            data["weight_" + str(a) + "_fund_" + str(fund.name)].append(fund.var.weights[a])
            data["exp_return_" + str(a) + "_fund_" + str(fund.name)].append(fund.exp.returns[a])

        #varcovar
        for idx_x, asset_x in enumerate(fund.var.covariance_matrix.columns):
            for idx_y, asset_y in enumerate(fund.var.covariance_matrix.columns):
                if idx_x <= idx_y:
                    data["var_covar_" +   "fund_" + str(fund.name)+ "_"  + str(asset_x) + "_"  + str(asset_y)].append(fund.var.covariance_matrix.loc[asset_x][asset_y])

    for i in Deltas:
        data[i].append(Deltas[i])

    data["FX_domestic_foreign"].append(environment.var.fx_rates.loc["domestic"]["foreign"]) #Todo: general case!

    return data

def reset_intraday(data):
    for key, value in data.iteritems():
        del value[:-1]
    return data
