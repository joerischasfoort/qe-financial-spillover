from objects.fund import *
from objects.asset import *
from functions.realised_returns import *
from functions.distribute import distribute_options_equally
from functions.stochasticprocess import *
from functions.realised_returns import *
import numpy as np
import pandas as pd


def init_objects(parameters):
    """
    Function to initialise the model objects: first assets, then funds
    :param parameters: object which holds all model parameters
    :return: list of fund objects, list of asset objects
    """
    asset_nationalities = distribute_options_equally(parameters.n_assets, parameters.regions)
    assets = []
    asset_return_variance = []
    for asset_n, nat in zip(range(parameters.n_assets), asset_nationalities):
        asset_params = AssetParameters(nat, parameters.face_value, parameters.default_rate,
                                       parameters.nominal_interest_rate, parameters.maturity, parameters.quantity)
        # initialise asset vars and historical vars from global params
        init_asset_vars = AssetVariables(parameters.init_asset_price)
        previous_assets_vars = AssetVariables(parameters.init_asset_price)
        assets.append(Asset(asset_n, init_asset_vars, previous_assets_vars, asset_params))
        # calculate initial variance of returns
        asset_return_variance.append(simulated_return_variance(assets[-1], parameters.days))

    # calculate initial asset vars for agent parameters
    asset_values = [asset.var.price * asset.par.quantity for asset in assets]
    default_rates = [asset.par.default_rate for asset in assets]
    returns = [realised_returns_domestic(asset.par.default_rate,
                                         asset.par.face_value,
                                         asset.var.price,
                                         asset.var.price,
                                         asset.par.quantity,
                                         asset.par.nominal_interest_rate,
                                         asset.par.maturity) for asset in assets]


    # create covariance matrix for assets
    covs = np.array([np.zeros(len(assets)) for x in range(len(assets))])
    # insert variance into the diagonal of the matrix
    for idx, var in enumerate(asset_return_variance):
        covs[idx][idx] = var

    covariance_matrix = pd.DataFrame(covs, index=assets, columns=assets)

    funds = []
    fund_nationalities = distribute_options_equally(parameters.n_funds, parameters.regions)

    def divide_by_funds(variable): return np.divide(variable, parameters.n_funds)

    for idx, nat in enumerate(fund_nationalities):
        fund_params = AgentParameters(nat, parameters.price_memory, parameters.fx_memory)
        asset_portfolio = {asset: divide_by_funds(value) for (asset, value) in zip(assets, asset_values)} #for every asset {asset: value}
        ewma_returns = {asset: rt for (asset, rt) in zip(assets, returns)}
        ewma_delta_prices = {asset: 0 for (asset, rt) in zip(assets, returns)}
        ewma_delta_fx = 0
        fund_vars = AgentVariables(asset_portfolio,
                                   divide_by_funds(parameters.total_money),
                                   sum(asset_portfolio.values()) + divide_by_funds(parameters.total_money),
                                   ewma_returns,
                                   ewma_delta_prices,
                                   ewma_delta_fx)
        r = ewma_returns.copy()
        df_rates = {asset: default_rate for (asset, default_rate) in zip(assets, default_rates)}
        fund_expectations = AgentExpectations(r, df_rates, parameters.init_exchange_rate, covariance_matrix)
        funds.append(Fund(idx, fund_vars, fund_vars, fund_params, fund_expectations))

    return assets, funds


def simulated_return_variance(asset, days): #TODO what to do with implied parameters for random process
    """
    Calculate an approximate variance for an asset by simulating the average underlying default probability
    :param asset: Asset object of interest
    :param days: integer amount of days over which to conduct the simulation
    :return: float initial variance of the asset
    """
    simulated_default_rates = ornstein_uhlenbeck_levels(time=days)
    simulated_returns = [realised_returns_domestic(df, V=asset.par.face_value ,P=1,
                                                   P_tau=1, Q=asset.par.quantity,
                                                   rho=asset.par.nominal_interest_rate,
                                                   m=asset.par.maturity) for df in simulated_default_rates]
    return np.var(simulated_returns)
