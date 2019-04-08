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


def init_objects_one_country(parameters, default_stats, seed):
    """
    Initializes model objects: currencies,
    :param parameters:
    :param seed:
    :return: list of assets, currencies, funds, exogenous agents, and an environment
    """
    # 1 initialize portfolios
    portfolios = []
    for idx in range(parameters["n_domestic_assets"]):
        asset_params = AssetParameters('domestic', parameters["face_value"],
                                       parameters["nominal_interest_rate"],
                                       parameters["maturity"], parameters["quantity"],
                                       default_stats, idx)
        init_asset_vars = AssetVariablesTime(parameters["face_value"] / float(parameters["quantity"]), init_default_rate=0)

        portfolios.append(Asset(idx, init_asset_vars, None, asset_params))

    # 2 initialize currencies
    currencies = [
        Currency("domestic", CurrencyParameters('domestic', parameters["currency_rate"], parameters["total_money"]))]

    # 3 simulate historical returns for portfolios & currencies:
    historical_returns = simulated_portfolio_returns_one_country(portfolios, parameters, seed)
    for c in currencies:
        historical_returns.append([c.par.nominal_interest_rate for t in range(parameters["end_day"] - parameters["start_day"])])

    # 4 initialize funds
    funds = []

    for idx in range(parameters["n_domestic_funds"]):
        # 3a determine parameters
        #TODO add heterogeneity here
        risk_aversion = {"domestic_assets": parameters["risk_aversion"]}
        fund_params = AgentParameters("domestic", parameters["price_memory"],
                                      None, risk_aversion,
                                      parameters["adaptive_param"], parameters["news_evaluation_error"])

        # 3b determine variables
        # compute initial variable values associated with portfolio shares
        asset_portfolio = {}
        ewma_returns = {}
        realised_rets = {}

        for a in portfolios:
            asset_portfolio.update({a: a.par.quantity})
            ewma_returns.update({a: a.par.nominal_interest_rate})  # the nominal interest rate is the initial return
            realised_rets.update({a: 0})

        # compute initial variable values associated with currencies
        currency_portfolio = {}
        losses = {}

        for currency in currencies:
            currency_portfolio.update({currency: currency.par.quantity})
            ewma_returns.update({currency: currency.par.nominal_interest_rate})  # the nominal interest rate is the initial return
            losses.update({currency: parameters["init_losses"]}) #TODO is this needed?

        # initialized as having no value
        init_c_profits = dict.fromkeys(currencies)
        init_a_profits = dict.fromkeys(portfolios)
        init_profits = init_c_profits.copy()  # start with x's keys and values
        init_profits.update(init_a_profits)

        # init co-variance matrix
        assets = portfolios + currencies

        cov_matr = calculate_covariance_matrix(historical_returns, assets)

        fund_redeemable_share_size = sum([asset_portfolio[a] * a.var.price[-1] for a in portfolios] + [currency_portfolio[c] for c in currencies])

        fund_vars = AgentVariablesTime(asset_portfolio,
                                       currency_portfolio,
                                       fund_redeemable_share_size,
                                       {},
                                       {},
                                       ewma_returns,
                                       {},
                                       {},
                                       cov_matr, parameters["init_payouts"], dict.fromkeys(assets),
                                       realised_rets, init_profits, losses,
                                       fund_redeemable_share_size,
                                       {}) # used to be currency_inventory

        # 3c initialising expectations
        r = ewma_returns.copy()
        cons_returns = {a: 0 for a in portfolios + currencies}
        df_rates = {a: a.var.default_rate for a in portfolios}
        exp_prices = {a: a.var.price for a in portfolios}
        exp_currency_returns = {currency: currency.par.nominal_interest_rate for currency in currencies}
        exp_inflation = {"domestic": parameters["domestic_inflation_mean"]}
        fund_expectations = AgentExpectations(r, cons_returns, r, df_rates, None, None, exp_prices,
                                              exp_currency_returns,
                                              exp_inflation)

        funds.append(Fund(idx, fund_vars, copy_agent_variables(fund_vars), fund_params, fund_expectations))

    # 5 initialize exogenous agents
    # create central bank
    cb_assets = {asset: 0 for asset in portfolios}
    cb_currency = {cur: sum(cb_assets.values()) for cur in currencies}

    asset_targets = {asset: 0 for asset in portfolios}
    cb_variables = CB_VariablesTime(cb_assets, cb_currency, 0, 0, asset_targets)
    central_bank = Central_Bank(cb_variables, None, ExoAgentParameters("domestic"))

    # create underwriter agent
    underwriter_assets = {asset: 0 for asset in portfolios}
    underwriter_currency = {currency: 0 for currency in currencies}
    underwriter_variables = ExoAgentVariablesTime(underwriter_assets, underwriter_currency, 0, 0)
    underwriter = Underwriter(underwriter_variables, None)

    exogenous_agents = {repr(central_bank): central_bank, repr(underwriter): underwriter}

    return portfolios, currencies, funds, exogenous_agents


def calculate_covariance_matrix(historical_stock_returns, assets):
    """
    Calculate the covariance matrix of a safe asset (money) provided stock returns
    :param historical_stock_returns: list of historical stock returns
    :return: DataFrame of the covariance matrix of stocks and money (in practice just the variance).
    """
    covariances = np.cov(historical_stock_returns)

    return pd.DataFrame(covariances, index=assets, columns=assets)
