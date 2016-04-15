import numpy as np
from probo.engines.pricingengine import PricingEngine

class Asian_MC(PricingEngine):
    """An arithmetic/geometric Asian Option using Monte Carlo Methods."""
    
    def __init__(self, nreps):
        self.__nreps = nreps
        
    def calculate(self, option):
        rate, spot, sigma, div = option.marketData
        disc_factor = np.exp(rate * option.expiry)
        dt = option.expiry
        z = np.random.normal(size=self.__nreps)
        
        nudt = (rate - 0.5 * sigma * sigma) * dt
        sidt = sigma * np.sqrt(dt)
        
        stock_path = spot * np.exp(nudt + sidt * z)
        asian_Ct = option.payoff(stock_path)
        # Need to take averages for strikes or asset values??
        
        
  
