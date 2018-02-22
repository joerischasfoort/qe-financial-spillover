from objects.fund import *
from objects.asset import *
from objects.parameters import *

def init_objects(global_parameters, init_asset_vars, previous_assets_vars, global_asset_params):
    """
    Function to initialise model if nescessary
    :param paramameters:
    :param inital_variables: dictionary of inital variables for 'assets' and for 'funds'
    :return: list of fund objects, list of asset objects
    """
    # specify types of assets
    nationalities = ['D', 'D', 'F', 'F']
    repayments_rates = ['high', 'low', 'high', 'low']
    default_rates = ['high', 'low', 'high', 'low']
    # initialise the assets
    assets = []
    for asset_n, nat, r_r, d_r in zip(range(global_parameters.n_assets), nationalities, repayments_rates, default_rates):
        asset_params = AssetParameters(nat, global_asset_params.face_value, d_r, r_r,
                                       global_asset_params.nominal_interest_rate, global_asset_params.asset_supply)
        assets.append(Asset(init_asset_vars, previous_assets_vars, asset_params))
    # initalise the funds
    funds = []
    # for fund_n in range(range(parameters.n_funds)):
    #     funds.append(Fund(inital_variables['funds'], previous_variables['funds'], parameters['funds']))

    # Attach regions to funds

    return funds, assets