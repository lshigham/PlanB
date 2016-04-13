import numpy as np
from probo.engines.pricingengine import PricingEngine

class NaiveMC(PricingEngine):
    """A Naive Monte Carlo Option Pricing Engine."""

    def __init__(self, nreps):
        self.__nreps = nreps

    def calculate(self, option):
        rate, spot, sigma, div = option.marketData
        disc = np.exp(rate * option.expiry)
        dt = option.expiry
        #z = np.random.normal(size=self.__nreps)
        for i in range(nreps):
            

        nudt = (rate - 0.5 * sigma * sigma) * dt
        sidt = sigma * np.sqrt(dt)

        St = np.zeros((self.__nreps, ))
        Ct = np.zeros((self.__nreps, ))
        St = spot * np.exp(nudt + sidt * z)
        Ct = option.payoff(St)
        price = disc * Ct.mean()

        return price