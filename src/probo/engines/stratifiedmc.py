import numpy as np
from scipy.stats import norm
from probo.engines.pricingengine import PricingEngine


class Stratified_mc(PricingEngine):
    """A Stratified Monte Carlo Option Pricing Engine."""

    def __init__(self, nreps):
        self.__nreps = nreps

    def calculate(self, option):
        rate, spot, sigma, div = option.marketData
        disc = np.exp(rate * option.expiry)
        dt = option.expiry 

        nudt = (rate - 0.5 * sigma * sigma) * dt
        sidt = sigma * np.sqrt(dt)

        St = np.zeros((self.__nreps, ))
        Ct = np.zeros((self.__nreps, ))
        
        #Stratified portion
        for i in range(nreps):
            u = np.random.uniform(size = 1)
            u_hat = (i + u) / nreps
            z = norm.ppf(uhat)
            St[i] = spot * np.exp(nudt + sidt * z)
            Ct[i] = option.payoff(St[i])
        
        price = disc * Ct.mean()
        se = Ct.std(dtype = np.float64) / np.sqrt(nreps)

        return Ct
        
