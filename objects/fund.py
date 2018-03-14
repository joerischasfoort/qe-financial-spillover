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
    def __init__(self, assets, currency, redeemable_shares, asset_demand, currency_demand,
                 ewma_returns, ewma_delta_prices, ewma_delta_fx, covariance_matrix, payouts,
                 weights, hypothetical_returns, total_profits):
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
        self.hypothetical_returns = hypothetical_returns
        self.total_profits = total_profits


class AgentParameters:
    """
    Holds the the agent parameters
    """
    def __init__(self, country, price_memory, fx_memory, risk_aversion, adaptive_param, news_evaluation_error,
                 target_growth):
        self.country = country
        self.price_memory = price_memory
        self.fx_memory = fx_memory
        self.risk_aversion = risk_aversion
        self.adaptive_param = adaptive_param
        self.news_evaluation_error = news_evaluation_error
        self.target_growth = target_growth


class AgentExpectations:
    """
    Holds the agent expectations for several variables
    """
    def __init__(self, returns, default_rates, exchange_rates, exp_prices, cash_returns):
        self.returns = returns
        self.default_rates = default_rates
        self.exchange_rates = exchange_rates
        self.prices = exp_prices
        self.cash_returns = cash_returns
