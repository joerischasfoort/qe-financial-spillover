from init_objects_4a import *
from spillover_model import *
import pickle

def initial_simulation(seed):
    list_of_risk_correlation = {}
    list_of_risk_correlation.update({'domestic_inflation' + "_and_" + 'foreign_inflation': 0.4})
    list_of_risk_correlation.update({'foreign_inflation' + "_and_" + 'domestic_inflation': list_of_risk_correlation[
        'domestic_inflation' + "_and_" + 'foreign_inflation']})
    list_of_risk_correlation.update({'domestic_inflation' + "_and_" + 'fx_shock': -0.0})
    # list_of_risk_correlation.update({'foreign_inflation'+"_and_" +'domestic_fx_shock': -0.17})

    # 1 setup parameters
    parameters = {  # Todo: cleaning and spell checking!!
        # global parameters
        "n_domestic_assets": 2,
        "n_foreign_assets": 2,
        "n_domestic_funds": 2,
        "n_foreign_funds": 2,
        "list_risk_corr": list_of_risk_correlation,
        "domestic_price_index": 1,
        "foreign_price_index": 1,
        "domestic_inflation_mean": 0.01 / float(250),
        "foreign_inflation_mean": 0.0285 / float(250),
        "domestic_inflation_std": 0.009 / float(250),
        "foreign_inflation_std": 0.013 / float(250),
        "start_day": 1,
        "end_day": 5001,
        "p_change_intensity": 0.0001,
        "fx_change_intensity": 0.0001,
        "cov_memory": 0.00,
        # asset parameters
        "face_value": 5000,
        "nominal_interest_rate": 0.02 / 250,
        "currency_rate": 0.0 / 250,
        "maturity": 0.9996,
        "quantity": 5000,
        # agent parameters
        "price_memory": 0.0,
        "fx_memory": 0.0,
        "fx_reversion_speed": 0.15 / 250,
        "local_currency_return_weight": 1,
        "risk_aversion": 5.0,
        "domestic_risk_aversion_D_asset": 5,
        "domestic_risk_aversion_F_asset": 5,
        "foreign_risk_aversion_D_asset": 5,
        "foreign_risk_aversion_F_asset": 5,
        "news_evaluation_error": 0,
        # cb parameters
        "cb_country": 'domestic',
        # initial values
        "init_asset_price": 1.0,
        "init_exchange_rate": 1.0,
        "total_money": 1000,
        "init_agent_ewma_delta_prices": 1,
        "init_ewma_delta_fx": 1,
        "init_asset_demand": 0,
        "init_currency_demand": 0,
        "init_payouts": 0,
        "init_losses": 0,
        "init_profits": 0,
        # shock processes parameters
        "fx_shock_mean": 0.0,
        "fx_shock_std": 0.0,
        "domestic_default_events_mean": 90 / float(250),
        "foreign_default_events_mean": 90 / float(250),
        "domestic_default_events_std": 5 / float(250),
        "foreign_default_events_std": 5 / float(250),
        "default_events_mean_reversion": 0.004,  # 0.001,
        "domestic_default_rate_mean": 0.01 / float(90),
        "foreign_default_rate_mean": 0.01 / float(90),
        "domestic_default_rate_std": 0,
        "foreign_default_rate_std": 0,
        "default_rate_mean_reversion": 1,
        'conv_bound': 0.01,
        "adaptive_param": 0.0
    }

    obj_label = "master"

    saving_params = {}
    saving_params.update({"path": 'C:\Users\jrr\Dropbox\GitHub\qe-financial-spillover\data\Objects'})
    saving_params.update({"time": 0})

    port_holdings = {"domestic_0": [1961, 930, 1651, 1821], "domestic_1": [3204, 571, 656, 75],
                     "foreign_0": [263, 556, 7045, 8461], 'foreign_1': [568, 78, 10009, 1692]}

    cur_holdings = {"domestic_0": [0, 0],
                    "domestic_1": [0, 0],
                    "foreign_0": [0, 0],
                    "foreign_1": [0, 0]}

    maturities = [0.99936, 1] * 2

    face_values = [sum(port_holdings[i][0] for i in port_holdings), sum(port_holdings[i][1] for i in port_holdings),
                   sum(port_holdings[i][2] for i in port_holdings), sum(port_holdings[i][3] for i in port_holdings)]
    quantities = face_values

    coupon_rates = [0.01 / 250, 0.02 / 250] * 2

    currency_rates = {"domestic": 0.002 / 250, "foreign": 0.0275 / 250}
    currency_amounts = {"domestic": sum(cur_holdings[i][0] for i in cur_holdings),
                        "foreign": sum(cur_holdings[i][1] for i in cur_holdings)}

    risk_aversions = {"domestic_risk_aversion_domestic_asset": [2, 2], "domestic_risk_aversion_foreign_asset": [5, 10],
                      "foreign_risk_aversion_domestic_asset": [5, 10], "foreign_risk_aversion_foreign_asset": [4, 4]}

    default_stats = {"mean_default_events": [15 / float(250), 15 / float(250), 75 / float(250), 75 / float(250)]}
    default_stats.update(
        {"default_events_std": [0.44 / float(250), 0.44 / float(250), 2.83 / float(250), 2.83 / float(250)]})
    default_stats.update(
        {"default_rate_mean": [0.005 / float(15), 0.02 / float(15), 0.005 / float(75), 0.02 / float(75)]})
    default_stats.update({"default_rate_std": [0, 0, 0, 0]})
    default_stats.update({"default_events_mean_reversion": [0.0011, 0.0011, 0.0014, 0.0014]})

    init_4a_inputs = [parameters, maturities, face_values, quantities, coupon_rates, currency_rates, currency_amounts,
                      port_holdings, cur_holdings, risk_aversions, default_stats, seed]

    # 2 initalise model objects
    portfolios, currencies, funds, environment, exogenous_agents = init_objects_4a(*init_4a_inputs)

    ra = {funds[0]: [2, 4, 2.4, 2, 2, 2.4], funds[1]: [0.9, 5, 4, 30, 0.9, 4], funds[2]: [30, 120, 1.4, 1.2, 30, 1.4],
          funds[3]: [15, 120, 0.9, 5.5, 15, 0.9]}
    ra = {funds[0]: [2, 2 * 5, 2 * 10, 2 * 10 * 5, 2, 2 * 10], funds[1]: [2, 2 * 5, 2 * 10, 2 * 10 * 5, 2, 2 * 10],
          funds[2]: [2 * 10, 2 * 10 * 2, 2, 2 * 2, 2 * 10, 2], funds[3]: [2 * 10, 2 * 10 * 2, 2, 2 * 2, 2 * 10, 2]}

    # including the full risk aversion matrix
    for f in funds:
        f.par.RA_matrix = f.var.covariance_matrix.copy()
        for row in range(len(f.par.RA_matrix.index)):  # 2 initalise model objects
            for col in range(len(f.par.RA_matrix.index)):
                f.par.RA_matrix.iloc[row, col] = np.sqrt(ra[f][row]) * np.sqrt(ra[f][col])



    # 3 simulate model

    portfolios, currencies, environment, exogenous_agents, funds, data_t = spillover_model(portfolios, currencies,
                                                                                           environment,
                                                                                           exogenous_agents, funds,
                                                                                           seed, obj_label,
                                                                                           saving_params)

    return portfolios, currencies, environment, exogenous_agents, funds









def load_first_run():
    data = open(
        'C:\Users\jrr\Dropbox\GitHub\qe-financial-spillover\data\Objects\objects_day_5000_seed_'+str(seed)+'_master.pkl',
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

    return portfolios_cal, currencies_cal, environment_cal, exogenous_agents_cal, funds_cal




def init_port_holdings_4f(seed):
    list_of_risk_correlation = {}
    list_of_risk_correlation.update({'domestic_inflation' + "_and_" + 'foreign_inflation': 0.4})
    list_of_risk_correlation.update({'foreign_inflation' + "_and_" + 'domestic_inflation': list_of_risk_correlation[
        'domestic_inflation' + "_and_" + 'foreign_inflation']})
    list_of_risk_correlation.update({'domestic_inflation' + "_and_" + 'fx_shock': -0.0})
    # list_of_risk_correlation.update({'foreign_inflation'+"_and_" +'domestic_fx_shock': -0.17})

    # 1 setup parameters
    parameters = {  # Todo: cleaning and spell checking!!
        # global parameters
        "n_domestic_assets": 2,
        "n_foreign_assets": 2,
        "n_domestic_funds": 2,
        "n_foreign_funds": 2,
        "list_risk_corr": list_of_risk_correlation,
        "domestic_price_index": 1,
        "foreign_price_index": 1,
        "domestic_inflation_mean": 0.01 / float(250),
        "foreign_inflation_mean": 0.0285 / float(250),
        "domestic_inflation_std": 0.009 / float(250),
        "foreign_inflation_std": 0.013 / float(250),
        "start_day": 1,
        "end_day": 5001,
        "p_change_intensity": 0.0001,
        "fx_change_intensity": 0.0001,
        "cov_memory": 0.00,
        # asset parameters
        "face_value": 5000,
        "nominal_interest_rate": 0.02 / 250,
        "currency_rate": 0.0 / 250,
        "maturity": 0.9996,
        "quantity": 5000,
        # agent parameters
        "price_memory": 0.0,
        "fx_memory": 0.0,
        "fx_reversion_speed": 0.15 / 250,
        "local_currency_return_weight": 1,
        "risk_aversion": 5.0,
        "domestic_risk_aversion_D_asset": 5,
        "domestic_risk_aversion_F_asset": 5,
        "foreign_risk_aversion_D_asset": 5,
        "foreign_risk_aversion_F_asset": 5,
        "news_evaluation_error": 0,
        # cb parameters
        "cb_country": 'domestic',
        # initial values
        "init_asset_price": 1.0,
        "init_exchange_rate": 1.0,
        "total_money": 1000,
        "init_agent_ewma_delta_prices": 1,
        "init_ewma_delta_fx": 1,
        "init_asset_demand": 0,
        "init_currency_demand": 0,
        "init_payouts": 0,
        "init_losses": 0,
        "init_profits": 0,
        # shock processes parameters
        "fx_shock_mean": 0.0,
        "fx_shock_std": 0.0,
        "domestic_default_events_mean": 90 / float(250),
        "foreign_default_events_mean": 90 / float(250),
        "domestic_default_events_std": 5 / float(250),
        "foreign_default_events_std": 5 / float(250),
        "default_events_mean_reversion": 0.004,  # 0.001,
        "domestic_default_rate_mean": 0.01 / float(90),
        "foreign_default_rate_mean": 0.01 / float(90),
        "domestic_default_rate_std": 0,
        "foreign_default_rate_std": 0,
        "default_rate_mean_reversion": 1,
        'conv_bound': 0.01,
        "adaptive_param": 0.0
    }

    obj_label = "master"

    saving_params = {}
    saving_params.update({"path": 'C:\Users\jrr\Dropbox\GitHub\qe-financial-spillover\data\Objects'})
    saving_params.update({"time": 0})

    port_holdings = {"domestic_0": [1961, 930, 1651, 1821], "domestic_1": [3204, 571, 656, 75],
                     "foreign_0": [263, 556, 7045, 8461], 'foreign_1': [568, 78, 10009, 1692]}

    cur_holdings = {"domestic_0": [0, 0],
                    "domestic_1": [0, 0],
                    "foreign_0": [0, 0],
                    "foreign_1": [0, 0]}

    maturities = [0.99936, 1] * 2

    face_values = [sum(port_holdings[i][0] for i in port_holdings), sum(port_holdings[i][1] for i in port_holdings),
                   sum(port_holdings[i][2] for i in port_holdings), sum(port_holdings[i][3] for i in port_holdings)]
    quantities = face_values

    coupon_rates = [0.01 / 250, 0.02 / 250] * 2

    currency_rates = {"domestic": 0.002 / 250, "foreign": 0.0275 / 250}
    currency_amounts = {"domestic": sum(cur_holdings[i][0] for i in cur_holdings),
                        "foreign": sum(cur_holdings[i][1] for i in cur_holdings)}

    risk_aversions = {"domestic_risk_aversion_domestic_asset": [2, 2], "domestic_risk_aversion_foreign_asset": [5, 10],
                      "foreign_risk_aversion_domestic_asset": [5, 10], "foreign_risk_aversion_foreign_asset": [4, 4]}

    default_stats = {"mean_default_events": [15 / float(250), 15 / float(250), 75 / float(250), 75 / float(250)]}
    default_stats.update(
        {"default_events_std": [0.44 / float(250), 0.44 / float(250), 2.83 / float(250), 2.83 / float(250)]})
    default_stats.update(
        {"default_rate_mean": [0.005 / float(15), 0.02 / float(15), 0.005 / float(75), 0.02 / float(75)]})
    default_stats.update({"default_rate_std": [0, 0, 0, 0]})
    default_stats.update({"default_events_mean_reversion": [0.0011, 0.0011, 0.0014, 0.0014]})

    init_4a_inputs = [parameters, maturities, face_values, quantities, coupon_rates, currency_rates, currency_amounts,
                      port_holdings, cur_holdings, risk_aversions, default_stats, seed]

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