class Fund():
    """Class holding fund properties"""
    def __init__(self, name, variables, previous_variables, parameters, expectations):
        self.name = name
        self.var = variables
        self.var_previous = previous_variables
        self.par = parameters
        self.exp = expectations

    def __repr__(self):
        return 'fund' + str(self.name)


class AgentVariables:
    """
    Holds the initial variables for the agents
    """
    def __init__(self, assets, money, redeemable_shares, ewma_returns, ewma_delta_prices, ewma_delta_fx):
        self.assets = assets
        self.money = money
        self.redeemable_shares = redeemable_shares
        self.ewma_returns = ewma_returns
        self.ewma_delta_prices = ewma_delta_prices
        self.ewma_delta_fx = ewma_delta_fx


class AgentParameters:
    """
    Holds the the agent parameters
    """
    def __init__(self, nationality, price_memory, fx_memory):
        self.nationality = nationality
        self.price_memory = price_memory
        self.fx_memory = fx_memory


class AgentExpectations:
    """
    Holds the agent expectations for several variables
    """
    def __init__(self, returns, default_rates, exchange_rate, covariance_matrix):
        self.returns = returns
        self.default_rates = default_rates
        self.exchange_rate = exchange_rate
        self.covariance_matrix = covariance_matrix