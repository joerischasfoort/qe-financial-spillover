from objects.fund import *
from objects.asset import *
from functions.distribute import *
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
    # 1 initialize assets
    assets = []
    total_assets = parameters["n_domestic assets"] + parameters["n_foreign_assets"]
    asset_nationalities = ordered_list_of_countries(parameters["n_domestic assets"], parameters["n_foreign_assets"])
    asset_return_variance = []
    asset_values = []
    default_rates = []
    returns = []

    for idx in range(total_assets):
        asset_params = AssetParameters(asset_nationalities[idx], parameters["face_value"],
                                       parameters["default_rate"], parameters["nominal_interest_rate"],
                                       parameters["maturity"], parameters["quantity"])
        init_asset_vars = AssetVariables(parameters["init_asset_price"])
        previous_assets_vars = AssetVariables(parameters["init_asset_price"])
        assets.append(Asset(idx, init_asset_vars, previous_assets_vars, asset_params))
        asset_return_variance.append(simulated_return_variance(assets[-1], parameters["days"]))
        asset_values.append(assets[idx].var.price * assets[idx].par.quantity)
        default_rates.append(assets[idx].par.default_rate)
        returns.append(realised_returns(assets[idx].par.default_rate, assets[idx].par.face_value,
                                        assets[idx].var.price, assets[idx].var.price,
                                        assets[idx].par.quantity, assets[idx].par.nominal_interest_rate,
                                        assets[idx].par.maturity))


    # 2 Create covariance matrix for assets
    covs = np.zeros((total_assets, total_assets))
    # insert variance into the diagonal of the matrix
    for idx, var in enumerate(asset_return_variance):
        covs[idx][idx] = var

    covariance_matrix = pd.DataFrame(covs, index=assets, columns=assets)

    # 3 Create funds
    funds = []
    total_funds = parameters["n_domestic_funds"] + parameters["n_foreign_funds"]
    fund_nationalities = ordered_list_of_countries(parameters["n_domestic_funds"], parameters["n_foreign_funds"])

    def divide_by_funds(variable): return np.divide(variable, total_funds)

    for idx in range(total_funds):
        fund_params = AgentParameters(fund_nationalities[idx], parameters["price_memory"],
                                      parameters["fx_memory"], parameters["risk_aversion"])
        asset_portfolio = {asset: divide_by_funds(value) for (asset, value) in zip(assets, asset_values)}
        ewma_returns = {asset: rt for (asset, rt) in zip(assets, returns)}
        ewma_delta_prices = {asset: parameters["init_agent_ewma_delta_prices"] for (asset, rt) in zip(assets, returns)}
        ewma_delta_fx = parameters["init_ewma_delta_fx"]
        fund_vars = AgentVariables(asset_portfolio,
                                   divide_by_funds(parameters["total_money"]),
                                   sum(asset_portfolio.values()) + divide_by_funds(parameters["total_money"]),
                                   ewma_returns,
                                   ewma_delta_prices,
                                   ewma_delta_fx,
                                   covariance_matrix)
        r = ewma_returns.copy()
        df_rates = {asset: default_rate for (asset, default_rate) in zip(assets, default_rates)}
        fund_expectations = AgentExpectations(r, df_rates, parameters["init_exchange_rate"], parameters["cash_return"])
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
    simulated_returns = [realised_returns(df, V=asset.par.face_value ,P=1,
                                                   P_tau=1, Q=asset.par.quantity,
                                                   rho=asset.par.nominal_interest_rate,
                                                   m=asset.par.maturity) for df in simulated_default_rates]
    return np.var(simulated_returns)
