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
def american_call_payoff(engine, spot, option):
    for i in range(engine.steps, 0, -1):        
        continuation_value = np.maximum(spot * (engine.u ** (engine.steps - i)) * (engine.d ** (i)) - option.strike, 0.0) 
        return np.maximum(np.maximum(spot - option.strike, 0.0), engine.pu *continuation_value[1:i+1] + engine.pd * continuation_value[0:i])
        
def american_put_payoff(option, spot, engine):
    put_continuation_value = np.maximum(option.strike - spot * engine.up_states * engine.down_states, 0.0)
    return np.maximum(np.maximum(option.strike - spot), put_continuation_value)


# Need to fix bugs    
def black_scholes_call_payoff(option, spot, engine, data):
    price = spot * np.exp(-dividend * option.expiry) * norm.cdf(d1) - option.strike * np.exp(-rate * option.expiry) * norm.cdf(d2)
    return price

def black_scholes_put_payoff(option, spot, engine, data):
    price = option.strike * np.exp(-rate * option.expiry) * norm.cdf(-d2) - spot * np.exp(-dividend * option.expiry) * norm.cdf(-d1)
    return price
    
def monte_carlo_call_payoff(option, spot):
    return np.maximum(spot - option.strike, 0.0)

def monte_carlo_put_payoff(option, spot):
    return np.maximum(option.strike - spot, 0.0)
    
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