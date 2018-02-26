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
    Holds the initial variables for the assets, for now empty
    """
    def __init__(self, price):
        self.price = price


class AssetParameters:
    """
    Holds the initial variables for the assets
    """
    def __init__(self, regions, face_value, default_rate, nominal_interest_rate, maturity, quantity):
        self.regions = regions
        self.face_value = face_value
        self.default_rate = default_rate
        self.nominal_interest_rate = nominal_interest_rate
        self.maturity = maturity
        self.quantity = quantity