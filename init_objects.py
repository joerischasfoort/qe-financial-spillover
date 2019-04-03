from functions.initialize_assets import *
from functions.initialize_environment import *
from functions.initialize_agents import *


def init_objects(parameters, seed):
    """
    Function to initialise the model objects: first assets, then funds
    :param parameters: object which holds all model parameters
    :return: list of fund objects, list of asset objects
    """
    # 1 initialize portfolios
    portfolios = init_portfolios(parameters)

    # 2 initialize currencies
    currencies = init_currencies(parameters)

    # 3 initialize environment
    environment = init_environment(currencies, parameters)

    # 4 initialize funds
    funds = init_funds(environment,portfolios, currencies, parameters, seed)

    # 5 initialize exogenous agents
    exogenous_agents = init_exogenous_agents(portfolios, currencies, parameters)

    return portfolios, currencies, funds, environment, exogenous_agents


def init_objects_one_country(parameters, seed):
    """
    Initializes model objects: currencies,
    :param parameters:
    :param seed:
    :return: list of assets, currencies, funds, exogenous agents, and an environment
    """
    # 1 initialize portfolios
    portfolios = []
    total_assets = parameters["n_domestic_assets"] + parameters["n_foreign_assets"]

    for idx in range(total_assets):
        asset_params = AssetParameters('domestic', parameters["face_value"],
                                       parameters["nominal_interest_rate"],
                                       parameters["maturity"], parameters["quantity"])
        init_asset_vars = AssetVariablesTime(parameters["init_asset_price"], init_default_rate=0)

        portfolios.append(Asset(idx, init_asset_vars, None, asset_params))

    # 2 initialize currencies
    currencies = [CurrencyParameters('domestic', parameters["currency_rate"], parameters["total_money"])]

    # 3 initialize funds
    funds = []
    total_funds = parameters["n_domestic_funds"]

    for idx in range(total_funds):
        risk_aversion = {"domestic_assets": parameters["domestic_risk_aversion_D_asset"]}
        fund_params = AgentParameters("domestic", parameters["price_memory"],
                                      parameters["fx_memory"], risk_aversion,
                                      parameters["adaptive_param"], parameters["news_evaluation_error"])

        # compute initial variable values associated with portfolio shares
        asset_portfolio = {}
        asset_demand = {}
        ewma_returns = {}
        ewma_delta_prices = {}
        realised_rets = {}

        for a in portfolios:
            # funds initially have a home bias of 100%
            asset_portfolio.update({a: a.par.quantity / sum([i == a.par.country for i in fund_countries])})

            asset_demand.update({a: 0})  # demand is initialized at zero (this does not effect anything)
            ewma_returns.update({a: a.par.nominal_interest_rate})  # the nominal interest rate is the initial return
            ewma_delta_prices.update({a: parameters[
                "init_agent_ewma_delta_prices"]})  # TODO: IS THIS STILL NEEDED? WHY IS THE INITIAL VALUE 1?
            realised_rets.update({a: 0})

        # compute initial variable values associated with currencies
        currency_portfolio = {}
        currency_inventory = {}
        currency_demand = {}
        ewma_delta_fx = {}
        losses = {}

        for currency in currencies:
            # funds initially have a home bias of 100%
            currency_portfolio.update({currency: currency.par.quantity / sum([i == currency.par.country for i in fund_countries])})
            currency_inventory.update({currency: 0})  # TODO: could this also be empty
            currency_demand.update({currency: parameters["init_currency_demand"]})  # Todo: could this be empty
            ewma_delta_fx.update({currency: parameters["init_ewma_delta_fx"]})  # TODO: Still needed?

            ewma_returns.update({currency: currency.par.nominal_interest_rate})  # the nominal interest rate is the initial return
            losses.update({currency: parameters["init_losses"]})

        # initialized as having no value
        init_c_profits = dict.fromkeys(currencies)
        init_a_profits = dict.fromkeys(portfolios)
        init_profits = init_c_profits.copy()  # start with x's keys and values
        init_profits.update(init_a_profits)

        assets = portfolios + currencies
        covs = np.zeros((len(assets), len(assets)))
        cov_matr = pd.DataFrame(covs, index=assets, columns=assets)

        fund_redeemable_share_size = [asset_portfolio[a] * a.var.price for a in portfolios] + [currency_portfolio[c] for c in currencies]
        fund_redeemable_share_size = sum(fund_redeemable_share_size)

        fund_vars = AgentVariablesTime(asset_portfolio,
                                       currency_portfolio,
                                       fund_redeemable_share_size,
                                       asset_demand,
                                       currency_demand,
                                       ewma_returns,
                                       ewma_delta_prices,
                                       ewma_delta_fx,
                                       cov_matr, parameters["init_payouts"], dict.fromkeys(assets),
                                       realised_rets, init_profits, losses,
                                       fund_redeemable_share_size,
                                       currency_inventory)

        # Initialising expectations
        r = ewma_returns.copy()
        cons_returns = {a: 0 for a in portfolios + currencies}
        df_rates = {a: a.var.default_rate for a in portfolios}
        exp_prices = {a: a.var.price for a in portfolios}
        exp_fx_returns = {currency: currency.par.nominal_interest_rate for currency in currencies}
        exp_inflation = {"domestic": parameters["domestic_inflation_mean"]}
        fund_expectations = AgentExpectations(r, cons_returns, r, df_rates, None, None, exp_prices,
                                              exp_fx_returns,
                                              exp_inflation)  # TODO: why is this called exp_fx_returns? In the object this variable is called cash return

        funds.append(Fund(idx, fund_vars, copy_agent_variables(fund_vars), fund_params, fund_expectations))

    # initialize the covariance matrix with simulated values
    simulated_time_series = simulated_asset_return(funds, portfolios, currencies, 10000,
                                                   parameters, seed)
    for fund in funds:
        for i in assets:
            for j in assets:
                fund.var.covariance_matrix.loc[i][j] = \
                np.cov(simulated_time_series[fund][i], simulated_time_series[fund][j])[0][1]

        fund.var_previous.covariance_matrix = fund.var.covariance_matrix.copy()

    # 5 initialize exogenous agents
    # create central bank
    cb_assets = {asset: 0 for asset in portfolios}
    cb_currency = {cur: sum(cb_assets.values()) for cur in currencies}

    asset_targets = {asset: 0 for asset in portfolios}
    cb_variables = CB_VariablesTime(cb_assets, cb_currency, 0, 0, asset_targets)
    central_bank = Central_Bank(cb_variables, None, ExoAgentParameters(parameters["cb_country"]))

    # create underwriter agent
    underwriter_assets = {asset: 0 for asset in portfolios}
    underwriter_currency = {currency: 0 for currency in currencies}
    underwriter_variables = ExoAgentVariablesTime(underwriter_assets, underwriter_currency, 0, 0)
    underwriter = Underwriter(underwriter_variables, None)

    exogenous_agents = {repr(central_bank): central_bank, repr(underwriter): underwriter}

    return portfolios, currencies, funds, exogenous_agents
