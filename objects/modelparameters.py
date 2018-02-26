class ModelParameters:
    """
    Holds the model parameters
    """
    def __init__(self, n_assets, n_funds, days, regions, price_memory, fx_memory, total_money,
                 face_value, default_rate, nominal_interest_rate, maturity, quantity,
                 init_asset_price, init_exchange_rate):
        # global parameters
        self.n_assets = n_assets
        self.n_funds = n_funds
        self.days = days
        self.regions = regions

        # asset parameters
        self.face_value = face_value
        self.default_rate = default_rate
        self.nominal_interest_rate = nominal_interest_rate
        self.maturity = maturity
        self.quantity = quantity

        # init asset variables
        self.init_asset_price = init_asset_price
        self.init_exchange_rate = init_exchange_rate

        # agent parameters
        self.price_memory = price_memory
        self.fx_memory = fx_memory

        # agent variables
        self.total_money = total_money


