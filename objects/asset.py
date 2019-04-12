class Asset():
    """Asset type class"""
    def __init__(self, name, variables, previous_variables, parameters):
        self.name = name
        self.var = variables
        self.var_previous = previous_variables
        self.par = parameters

    def __repr__(self):
        return 'asset' + str(self.name)


class AssetVariables:
    """
    Holds the initial variables for the assets
    """
    def __init__(self, price, default_rate):
        self.price = price
        self.default_rate = default_rate


class AssetVariablesTime:
    """
    Holds the initial variables for the assets as well as their historical values
    """
    def __init__(self, init_prices, init_default_rate, init_returns, fundamental_expected_default_rates):
        self.price = init_prices
        self.default_rate = init_default_rate
        self.returns = init_returns
        self.f_exp_dr = fundamental_expected_default_rates


class AssetParameters:
    """
    Holds the initial variables for the assets
    """
    def __init__(self, country, face_value, nominal_interest_rate, maturity, quantity, default_stats, idx):
        self.country = country
        self.face_value = face_value
        self.nominal_interest_rate = nominal_interest_rate
        self.maturity = maturity
        self.quantity = quantity
        self.mean_default_events = default_stats["mean_default_events"][idx]
        self.default_events_std = default_stats["default_events_std"][idx]
        self.default_rate_mean = default_stats["default_rate_mean"][idx]
        self.default_rate_std = default_stats["default_rate_std"][idx]
        self.default_events_mean_reversion = default_stats["default_events_mean_reversion"][idx]
