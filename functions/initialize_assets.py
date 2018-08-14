from objects.asset import *
from objects.currency import *
from functions.distribute import *
import numpy as np

def init_portfolios(parameters):


    portfolios = []

    total_assets = parameters["n_domestic_assets"] + parameters["n_foreign_assets"]

    asset_countries = ordered_list_of_countries(parameters["n_domestic_assets"], parameters["n_foreign_assets"])


    for idx in range(total_assets):
        asset_params = AssetParameters(asset_countries[idx], parameters["face_value"],
                                       parameters["nominal_interest_rate"],
                                       parameters["maturity"], parameters["quantity"])

        init_asset_vars = AssetVariables(parameters["init_asset_price"],
                                         0  # initial default rate
                                         )

        previous_assets_vars = AssetVariables(parameters["init_asset_price"],
                                              0  # initial default rate
                                              )

        portfolios.append(Asset(idx, init_asset_vars, previous_assets_vars, asset_params))

    return portfolios



def init_currencies(parameters):

    currencies = []
    total_currency = parameters["total_money"]
    asset_countries = ordered_list_of_countries(parameters["n_domestic_assets"], parameters["n_foreign_assets"])


    for idx, country in enumerate(set(asset_countries)):
        currency_param = CurrencyParameters(country, parameters["currency_rate"],
                                            np.divide(total_currency, len(set(asset_countries))))
        currencies.append(Currency(idx, currency_param))

    return currencies