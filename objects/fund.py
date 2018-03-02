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
    
    def get_demand(self, asset): #Equation 1.14 to 1.16
        pass
        


class AgentVariables:
    """
    Holds the initial variables for the agents
    """
    def __init__(self, assets, currency, redeemable_shares, asset_demand, currency_demand,
                 ewma_returns, ewma_delta_prices, ewma_delta_fx, covariance_matrix, payouts, weights, asset_xfx):
        self.assets = assets
        self.currency = currency
        self.redeemable_shares = redeemable_shares
        self.asset_demand = asset_demand
        self.currency_demand = currency_demand
        self.ewma_returns = ewma_returns
        self.ewma_delta_prices = ewma_delta_prices
        self.ewma_delta_fx = ewma_delta_fx
        self.covariance_matrix = covariance_matrix
        self.weights = weights
        self.payouts = payouts
        self.asset_xfx = asset_xfx


class AgentParameters:
    """
    Holds the the agent parameters
    """
    def __init__(self, nationality, price_memory, fx_memory, risk_aversion):
        self.nationality = nationality
        self.price_memory = price_memory
        self.fx_memory = fx_memory
        self.risk_aversion = risk_aversion


class AgentExpectations:
    """
    Holds the agent expectations for several variables
    """
    def __init__(self, returns, default_rates, exchange_rate, cash_returns):
        self.returns = returns
        self.default_rates = default_rates
        self.exchange_rate = exchange_rate
        self.cash_returns = cash_returns
