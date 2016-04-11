import numpy as np
from scipy.stats import norm
from probo.engines.pricingengine import PricingEngine
from probo.payoffs.payoff import PayoffType

class BlackScholes(PricingEngine):
    """The Black-Scholes-Merton pricing model for plain vanilla European options."""

    def calculate(self, option):
        rate, spot, sigma, div = option.marketData
        strike = option.strike
        expiry = option.expiry

        d1 = (np.log(spot/strike) + (rate - div + 0.5 * sigma * sigma) * expiry) / (sigma * np.sqrt(expiry))
        d2 = d1 - sigma * np.sqrt(expiry)

        if(option.payoffType is PayoffType.call):
            price = spot * np.exp(-div * expiry) * norm.cdf(d1) - strike * np.exp(-rate * expiry) * norm.cdf(d2)
        elif(option.payoffType is PayoffType.put):
            price = strike * np.exp(-rate * expiry) * norm.cdf(-d2) - spot * np.exp(-div * expiry) * norm.cdf(-d1)
        else:
            raise ValueError("Wrong Payoff Type") 

        return price


