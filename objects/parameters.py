class Parameters:
    """
    Holds the model parameters
    """
    def __init__(self, n_assets, n_funds, days, regions, price_memory, fx_memory, total_money,
                 face_value, default_rate, repayment_rate, nominal_interest_rate, quantity, init_asset_price):
        # global parameters
        self.n_assets = n_assets
        self.n_funds = n_funds
        self.days = days
        self.regions = regions

        # asset parameters
        self.face_value = face_value
        self.default_rate = default_rate
        self.repayment_rate = repayment_rate
        self.nominal_interest_rate = nominal_interest_rate
        self.quantity = quantity

        # init asset variables
        self.init_asset_price = init_asset_price

        # agent parameters
        self.price_memory = price_memory
        self.fx_memory = fx_memory

        # agent variables
        self.total_money = total_money


class AgentVariables:
    """
    Holds the initial variables for the agents
    """
    def __init__(self, assets, money, redeemable_shares):
        self.assets = assets
        self.money = money
        self.redeemable_shares = redeemable_shares


class AgentParameters:
    """
    Holds the the agent parameters
    """
    def __init__(self, nationality, price_memory, fx_memory):
        self.nationality = nationality
        self.price_memory = price_memory
        self.fx_memory = fx_memory


class AssetVariables:
    """
    Holds the initial variables for the assets, for now empty
    """
    def __init__(self, price):
        self.price = price


class AssetParameters:
    """
    Holds the initial variables for the assets
    """
    def __init__(self, regions, face_value, default_rate, repayment_rate, nominal_interest_rate, quantity):
        self.regions = regions
        self.face_value = face_value
        self.default_rate = default_rate
        self.repayment_rate = repayment_rate
        self.nominal_interest_rate = nominal_interest_rate
        self.quantity = quantity
