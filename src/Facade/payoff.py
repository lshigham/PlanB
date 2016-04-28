import numpy as np
from scipy.stats import norm
import Facade

class Vanilla_Payoff(Facade.OptionFacade):
    def __init__(self, expiry, strike, payoff):
        self.__expiry = expiry
        self.__strike = strike
        self.__payoff = payoff
        
    @property
    def expiry(self):
        return self.__expiry

    @expiry.setter
    def expiry(self, new_expiry):
        self.__expiry = new_expiry
    
    @property 
    def strike(self):
        return self.__strike
    
    @strike.setter
    def strike(self, new_strike):
        self.__strike = new_strike

    def payoff(self, spot):
        return self.__payoff(self, spot)
    
def call_payoff(option, spot):
    return np.maximum(spot - option.strike, 0.0)

def put_payoff(option, spot):
    return np.maximum(option.strike - spot, 0.0)

# Need to fix bugs    
def black_scholes_call_payoff(option, spot, data, engine):
    price = spot * np.exp(-data.dividend * option.expiry) * norm.cdf(engine.d1) - option.strike * np.exp(data.rate * option.expiry) * norm.cdf(engine.d2)
    return price

def black_scholes_put_payoff(option, spot, engine, data):
    price = option.strike * np.exp(-rate * option.expiry) * norm.cdf(-d2) - spot * np.exp(-dividend * option.expiry) * norm.cdf(-d1)
    return price
    
class Exotic_Payoff(Facade.OptionFacade):
    def __init__(self, expiry, strike, payoff):
        self.__expiry = expiry
        self.__strike = strike
        self.__payoff = payoff
        
    @property
    def expiry(self):
        return self.__expiry

    @expiry.setter
    def expiry(self, new_expiry):
        self.__expiry = new_expiry
    
    @property 
    def strike(self):
        return self.__strike
    
    @strike.setter
    def strike(self, new_strike):
        self.__strike = new_strike

    def payoff(self, spot):
        return self.__payoff(self, spot)
        
def arithmetic_asian_call_payoff(option, spot):
    pass

def arithmetic_asian_put_payoff(option, spot):
    pass