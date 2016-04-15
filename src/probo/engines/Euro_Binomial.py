
# Import as needed
import numpy as np
from probo.engines.pricingengine import PricingEngine
from scipy.stats import binom

# Creating Class using PricingEngine as MetaClass
class Euro_Binomial(PricingEngine):
    """The Binomial Pricing model for plain vanilla European options."""

# Creating init function
    def __init__(self, nreps):
        self.__nreps = nreps

#Where the calculation of the option prices are done.
    def calculate(self, option):
        if(option.payoffType is PayoffType.call):
            for i in range(node_number):
                spot_T = spot * (u ** (nreps - i)) * (d ** (i))
                call_T += option.payoff(spot_T, strike) * binom.pmf(nreps - i, nreps, pu)
            call_price = call_T * np.exp(-rate * expiry)
            return call_price
        elif(option.payoffType is PayoffType.put):
            for i in range(node_number):
                spot_T = spot * (u ** (nreps - i)) * (d ** (i))
                put_T += option.payoff(spot_T, strike) * binom.pmf(nreps - i, nreps, pd)
            put_price = put_T * np.exp(-rate * expiry)
            return put_price
        else:
            raise ValueError("Wrong Payoff Type")

        
    # Gathering data
    def main(self, option):
        rate, spot, sigma, div = option.marketData
        strike = option.strike
        expiry = option.expiry
        nreps = 2
        node_number = nreps + 1
        spot_T = 0.0
        price = 0.0
        dt = expiry / steps
        u = np.exp((rate - div)*dt + sigma * np.sqrt(dt)) 
        d = np.exp((rate - div)*dt - sigma * np.sqrt(dt))
        pu = (np.exp(-rate * expiry) - d) / (u - d)
        pd = 1 - pu
        
        call_price = calculate(self, option)
        put_price = calculate(self, option)
        
        print("The price is: {}".format(call_price))
        print("The price is: {}".format(put_price))
