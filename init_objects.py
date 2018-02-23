from objects.fund import *
from objects.asset import *
from objects.parameters import *
from functions.distribute import distribute_options_equally
import numpy as np


def init_objects(parameters):
    """
    Function to initialise the model objects: first assets, then funds
    :param parameters: object which holds all model parameters
    :return: list of fund objects, list of asset objects
    """
    asset_nationalities = distribute_options_equally(parameters.n_assets, parameters.regions)
    assets = []
    for asset_n, nat in zip(range(parameters.n_assets), asset_nationalities):
        asset_params = AssetParameters(nat, parameters.face_value, parameters.default_rate,
                                       parameters.repayment_rate,
                                       parameters.nominal_interest_rate, parameters.quantity)
        # initialise asset vars and historical vars from global params
        init_asset_vars = AssetVariables(parameters.init_asset_price)
        previous_assets_vars = AssetVariables(parameters.init_asset_price)
        assets.append(Asset(init_asset_vars, previous_assets_vars, asset_params))
    asset_values = [asset.var.price * asset.par.quantity for asset in assets]

    funds = []
    fund_nationalities = distribute_options_equally(parameters.n_funds, parameters.regions)

    def divide_by_funds(variable): return np.divide(variable, parameters.n_funds)

    for nat in fund_nationalities:
        fund_params = AgentParameters(nat, parameters.price_memory, parameters.fx_memory)
        asset_portfolio = {asset: divide_by_funds(value) for (asset, value) in zip(assets, asset_values)} #for every asset {asset: value}
        fund_vars = AgentVariables(asset_portfolio,
                                   divide_by_funds(parameters.total_money),
                                   sum(asset_portfolio.values()) + divide_by_funds(parameters.total_money))
        funds.append(Fund(fund_vars, fund_vars, fund_params))

    return assets, funds
