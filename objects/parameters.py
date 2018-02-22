class Parameters:
    """
    Holds the model parameters
    """
    def __init__(self, n_assets, n_funds, days, lambdas, theta, phi, regions, std_noise, ms, rho, omega, face_value, global_supply):
        self.n_assets = n_assets
        self.n_funds = n_funds
        self.days = days
        self.lambdas = lambdas
        self.theta = theta
        self.phi = phi
        self.regions = regions
        self.std_noise = std_noise
        self.ms = ms
        self.rho = rho
        self.omega = omega
        self.face_value = face_value


class AgentInitialVariables:
    """
    Holds the initial variables for the agents
    """
    def __init__(self, nationality, dm_portfolio1, dm_portfolio2, f_portfolio1, f_portfolio2, money):
        self.nationality = nationality
        self.domestic_portfolio1 = dm_portfolio1
        self.domestic_portfolio2 = dm_portfolio2
        self.foreign_portfolio1 = f_portfolio1
        self.foreign_portfolio2 = f_portfolio2
        self.money = money


class AgentParameters:
    """
    Holds the initial variables for the agents
    """
    def __init__(self, nationality, dm_portfolio1, dm_portfolio2, f_portfolio1, f_portfolio2, money):
        self.nationality = nationality
        self.domestic_portfolio1 = dm_portfolio1
        self.domestic_portfolio2 = dm_portfolio2
        self.foreign_portfolio1 = f_portfolio1
        self.foreign_portfolio2 = f_portfolio2
        self.money = money


class AssetInitialVariables:
    """
    Holds the initial variables for the assets, for now empty
    """
    def __init__(self, price):
        self.price = price


class AssetParameters:
    """
    Holds the initial variables for the assets
    """
    def __init__(self, nationality, face_value, default_rate, repayment_rate, nominal_interest_rate, asset_supply):
        self.nationality = nationality
        self.face_value = face_value
        self.default_rate = default_rate
        self.repayment_rate = repayment_rate
        self.nominal_interest_rate = nominal_interest_rate
        self.asset_supply = asset_supply