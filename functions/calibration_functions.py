from init_objects_4a import *
import pickle

def load_first_run():
    data = open(
        'C:\Users\jrr\Dropbox\GitHub\qe-financial-spillover\data\Objects\objects_day_5000_seed_1_masterNOC.pkl',
        'rb')

    list_of_objects = pickle.load(data)


    portfolios_cal = list_of_objects[0]
    currencies_cal = list_of_objects[1]
    environment_cal = list_of_objects[2]
    exogenous_agents_cal = list_of_objects[3]
    funds_cal = list_of_objects[4]


    data.close()

    parameters_cal = environment_cal.par.global_parameters
    parameters_cal["start_day"] = 1
    parameters_cal["end_day"] = 2

    return portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal, funds_cal, parameters_cal




def init_port_holdings_4f(parameters,seed):
    port_holdings = {"domestic_0": [1961, 930, 1651, 1821], "domestic_1": [3204, 571, 656, 75],
                     "foreign_0": [263, 556, 7045, 8461], 'foreign_1': [568, 78, 10009, 1692]}

    cur_holdings = {"domestic_0": [(200/float(39541))*6363, (2500/float(39541))*6363],
                    "domestic_1": [(200/float(39541))*4506, (2500/float(39541))*4506],
                    "foreign_0": [(200/float(39541))*16325, (2500/float(39541))*16325],
                    "foreign_1": [(200/float(39541))*12347, (2500/float(39541))*12347]}

    cur_holdings = {"domestic_0": [(0/float(39541))*6363, (0/float(39541))*6363],
                    "domestic_1": [(0/float(39541))*4506, (0/float(39541))*4506],
                    "foreign_0": [(0/float(39541))*16325, (0/float(39541))*16325],
                    "foreign_1": [(0/float(39541))*12347, (0/float(39541))*12347]}

    maturities = [0.99936, 1] * 2
    face_values = [sum(port_holdings[i][0] for i in port_holdings), sum(port_holdings[i][1] for i in port_holdings),
                   sum(port_holdings[i][2] for i in port_holdings), sum(port_holdings[i][3] for i in port_holdings)]
    quantities = face_values

    coupon_rates = [0.01 / 250, 0.02 / 250] * 2
    currency_rates = {"domestic": 0, "foreign": 0.00117 / 250}
    currency_amounts = {"domestic": sum(cur_holdings[i][0] for i in cur_holdings),
                        "foreign": sum(cur_holdings[i][1] for i in cur_holdings)}

    risk_aversions = {"domestic_risk_aversion_domestic_asset": [2, 2], "domestic_risk_aversion_foreign_asset": [2, 2],
                      "foreign_risk_aversion_domestic_asset": [2, 2], "foreign_risk_aversion_foreign_asset": [2, 2]}

    init_4a_inputs = [parameters, maturities, face_values, quantities, coupon_rates, currency_rates, currency_amounts,
                      port_holdings, cur_holdings, risk_aversions, seed]

    # 2 initalise model objects
    portfolios, currencies, funds, environment, exogenous_agents = init_objects_4a(*init_4a_inputs)

    environment.par.global_parameters["start_day"] = 1
    environment.par.global_parameters["end_day"] = 2

    return   portfolios, currencies, funds, environment, exogenous_agents



def approach_prices(portfolios, approach_speed):
    for a in portfolios:
        a.var.price = a.var.price + approach_speed*(1-a.var.price)

    return portfolios


def recompute_liabilities(f,portfolios,currencies, environment):
    s = sum(f.var.assets[a]*a.var.price*environment.var.fx_rates.loc[f.par.country][a.par.country] for a in portfolios)
    s+= sum(f.var.currency[c]*environment.var.fx_rates.loc[f.par.country][c.par.country] for c in currencies)

    return s



def approach_balance_sheets(funds_cal,portfolios_cal, currencies_cal, environment_cal, funds_init, portfolios_init, currencies_init, cur_dummy):
    for fi, fc in zip(funds_init, funds_cal):
        fc.var.asset_diff = {ac: fi.var.assets[ai] - fc.var.assets[ac] for ai, ac in
                             zip(portfolios_init, portfolios_cal)}
        fc.var.currency_diff = {cc: fi.var.currency[ci] - fc.var.currency[cc] for ci, cc in
                                zip(currencies_init, currencies_cal)}

    for f in funds_cal:
        f.var.asset_change = {}
        for a in portfolios_cal:
            f.var.asset_change[a] = f.var.asset_diff[a] * float(1)
        for c in currencies_cal:
            f.var.asset_change[c] = f.var.currency_diff[c] * float(1)

    for f in funds_cal:
        f.var.new_assets = {}
        f.var.new_currency = {}
        for a in portfolios_cal:
            f.var.new_assets.update({a: f.var.assets[a] + f.var.asset_change[a]})
        for c in currencies_cal:
            f.var.new_currency.update({c: f.var.currency[c] + f.var.asset_change[c]})
        f.var.assets = f.var.new_assets
        f.var_previous.assets = f.var.new_assets
        if cur_dummy == 1:
            f.var.currency = f.var.new_currency
            f.var_previous.currency = f.var.new_currency

    for f in funds_cal:
        s = recompute_liabilities(f, portfolios_cal, currencies_cal, environment_cal)
        f.var_previous.redeemable_shares = s


    return funds_cal



def save_progress(funds_cal, portfolios_cal,convergence_h, convergence_r, convergence_c):
    holding_diff = []
    for a in portfolios_cal:
        holding_diff.append(sum([abs(f.var.asset_diff[a]) for f in funds_cal]))

    holding_diff = [sum(holding_diff)]
    ret = [funds_cal[0].exp.returns[portfolios_cal[0]]]
    cov = [funds_cal[0].var.covariance_matrix.iloc[0, 0]]
    convergence_h = convergence_h.append(holding_diff)
    convergence_r = convergence_r.append(ret)
    convergence_c = convergence_c.append(cov)

    writer = pd.ExcelWriter('progressH.xlsx')
    convergence_h.to_excel(writer, 'Sheet1')
    writer.save()
    writer = pd.ExcelWriter('progressR.xlsx')
    convergence_r.to_excel(writer, 'Sheet1')
    writer.save()
    writer = pd.ExcelWriter('progressC.xlsx')
    convergence_c.to_excel(writer, 'Sheet1')
    writer.save()

    return convergence_h, convergence_r, convergence_c