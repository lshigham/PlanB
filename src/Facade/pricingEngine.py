import abc
import numpy as np
from scipy.stats import binom, norm
import Facade

class Pricing_Engine(object, metaclass=abc.ABCMeta):
    
    @abc.abstractmethod
    def calculate(self):
        """A method to implement a pricing model.

           The pricing method may be either an analytic model (i.e.
           Black-Scholes), a PDF solver such as the finite difference method,
           or a Monte Carlo pricing algorithm.
        """
        pass
        
class BinomialPricingEngine(Pricing_Engine):
    def __init__(self, steps, pricer):
        self.__steps = steps
        self.__pricer = pricer

    @property
    def steps(self):
        return self.__steps

    @steps.setter
    def steps(self, new_steps):
        self.__steps = new_steps
    
    def calculate(self, option, data):
        return self.__pricer(self, option, data)

    
def EuropeanBinomialPricer(engine, option, data):
    expiry = option.expiry
    strike = option.strike
    (spot, rate, volatility, dividend) = data.get_data()
    steps = engine.steps
    nodes = steps + 1
    dt = expiry / steps 
    u = np.exp((rate * dt) + volatility * np.sqrt(dt)) 
    d = np.exp((rate * dt) - volatility * np.sqrt(dt))
    pu = (np.exp(rate * dt) - d) / (u - d)
    pd = 1 - pu
    disc = np.exp(-rate * expiry)
    spotT = 0.0
    payoffT = 0.0
    
    for i in range(nodes):
        spotT = spot * (u ** (steps - i)) * (d ** (i))
        payoffT += option.payoff(spotT)  * binom.pmf(steps - i, steps, pu)  
    price = disc * payoffT 
     
    return price 


# Need to fix bugs
def AmericanBinomialPricer(engine, option, data):
    expiry = option.expiry
    strike = option.strike
    (spot, rate, volatility, dividend) = data.get_data()
    steps = engine.steps
    nodes = steps + 1
    delta_t = expiry / steps
    u = np.exp((rate * delta_t) + volatility * np.sqrt(delta_t))
    d = np.exp((rate * delta_t) - volatility * np.sqrt(delta_t))
    pu = (np.exp(rate * delta_t) - d) / (u - d)
    pd = 1 - pu
    #pu = 0.5 + 0.5 * (nu * delta_t / dxu)
    
    #disc = np.exp(-rate * expiry)
    discount_rate = np.exp(-rate * delta_t)
    nu = rate - 0.5 * volatility * volatility
    dxu = np.sqrt(volatility * volatility * delta_t + nu*nu*delta_t*delta_t)
    dxd = -dxu
    dpu = discount_rate * pu
    dpd = discount_rate * pd
    edxud = np.exp(dxu - dxd)
    edxd = np.exp(dxd)
    
    spot_t = []
    payoff_t = []
    spot_t.append(spot * np.exp(steps * dxd))
    #for a put -- need to generalize
    payoff_t.append(np.maximum(0.0, strike - spot_t[0]))
    for j in range(steps):
        spot_t.append(spot_t[-1] * edxud)
        payoff_t.append(np.maximum(0.0, strike - spot_t[j+1]))
    
    for i in range(steps-1, -1, -1):
        for j in range(i+1):
            payoff_t[j] = dpd*payoff_t[j] + dpu * payoff_t[j+1]
            spot_t[j] = spot_t[j]/edxd
            
            payoff_t[j] = np.maximum(payoff_t[j], strike - spot_t[j])
            
    price = discount_rate * payoff_t[j]
    return price

class BlackScholesPricingEngine(Pricing_Engine):
    def __init__(self, steps, pricer):
        self.__steps = steps
        self.__pricer = pricer

    @property
    def steps(self):
        return self.__steps

    @steps.setter
    def steps(self, new_steps):
        self.__steps = new_steps
    
    def calculate(self, option, data):
        return self.__pricer(self, option, data)


# Need to fix bugs
def Black_Scholes_Pricer(engine, option, data):
    expiry = option.expiry
    strike = option.strike
    (spot, rate, volatility, dividend) = data.get_data()
    d1 = (np.log(spot/strike) + (rate - dividend + 0.5 * volatility * volatility) * expiry) / (volatility * np.sqrt(expiry))
    d2 = d1 - volatility * np.sqrt(expiry)

class MonteCarloPricingEngine(Pricing_Engine):
    def __init__(self, steps, pricer):
        self.__steps = steps
        self.__pricer = pricer

    @property
    def steps(self):
        return self.__steps

    @steps.setter
    def steps(self, new_steps):
        self.__steps = new_steps
    
    def calculate(self, option, data):
        return self.__pricer(self, option, data)
        
        
def Naive_Monte_Carlo_Pricer(engine, option, data):
    expiry = option.expiry
    strike = option.strike
    (spot, rate, volatility, dividend) = data.get_data()
    steps = engine.steps
    discount_rate = np.exp(rate * expiry)
    delta_t = expiry
    z = np.random.normal(size = steps)
    
    nudt = (rate - 0.5 * volatility * volatility) * delta_t
    sidt = volatility * np.sqrt(delta_t)
    
    spot_t = np.zeros((steps, ))
    payoff_t = np.zeros((steps, ))
    spot_t = spot * np.exp(nudt + sidt * z)
    payoff_t = option.payoff(spot_t)
    price = discount_rate * payoff_t.mean()
    
    return price
    
def Stratified_Monte_Carlo_Pricer(engine, option, data):
    expiry = option.expiry
    strike = option.strike
    (spot, rate, volatility, dividend) = data.get_data()
    steps = engine.steps
    discount_rate = np.exp(-rate * expiry)
    delta_t = expiry
    
    nudt = (rate - 0.5 * volatility * volatility) * delta_t
    sidt = volatility * np.sqrt(delta_t)
    
    spot_t = np.zeros((steps, ))
    payoff_t = np.zeros((steps, ))
    
    for i in range(steps):
        u = np.random.uniform(size = 1)
        u_hat = (i + u) / steps
        z = norm.ppf(u_hat)
        spot_t[i] = spot * np.exp(nudt + sidt * z)
        payoff_t[i] = option.payoff(spot_t[i])
        
    price = discount_rate * payoff_t.mean()
    
    return price
    
def Antithetic_Monte_Carlo_Pricer(engine, option, data):
    expiry = option.expiry
    strike = option.strike
    (spot, rate, volatility, dividend) = data.get_data()   
    steps = engine.steps
    discount_rate = np.exp(-rate * expiry)
    delta_t = expiry
    z = np.random.normal(size = steps)

    nudt = (rate - 0.5 * volatility * volatility) * delta_t
    sidt = volatility * np.sqrt(delta_t)    
    
    spot_t_antithetic = np.zeros((steps, ))
    payoff_t_antithetic = np.zeros((steps, ))
    spot_t_antithetic = spot * np.exp(nudt - sidt * z)
    payoff_t_antithetic = option.payoff(spot_t_antithetic)
    
    price = discount_rate * payoff_t_antithetic.mean()
    
    return price


# Do I want to make a path dependent class?
# If so, what will I want to include?
    
def Asian_Option_Pricer(engine, option, data):
    expiry = option.expiry
    strike = option.strike
    (spot, rate, volatility, dividend) = data.get_data()
    steps = engine.steps
    discount_rate = np.exp(-rate * expiry)
    delta_t = expiry
    z = np.random.normal(size = steps)
    
    nudt = (rate - 0.5 * volatility * volatility) * delta_t
    sidt = volatility * np.sqrt(delta_t)    
    
    spot_t = np.zeros((steps, ))
    payoff_t = np.zeros((steps, ))

    for i in range(steps):
        spot_t[i] = spot_t[i-1] * nudt + sidt * z[i]
        payoff_t[i] = option.payoff(spot_t[i])
        
    price = discount_rate * payoff_t.mean()
    
    return price
    
    
def Lookback_Option_Pricer(engine, option, data):
    expiry = option.expiry
    strike = option.strike
    (spot, rate, volatility, dividend) = data.get_data()
    steps = engine.steps
    discount_rate = np.exp(-rate * expiry)
    delta_t = expiry
    z = np.random.normal(size = steps)
    
    nudt = (rate - 0.5 * volatility * volatility) * delta_t
    sidt = volatility * np.sqrt(delta_t)    
    
    spot_t = np.zeros((steps, ))
    payoff_t = np.zeros((steps, ))
    
    for i in range(steps):
        spot_t[i] = spot * nudt + sidt * z[i]
        payoff_t[i] = option.payoff(spot_t[i])
        
    price = discount_rate * payoff_t.max()   
    
    return price
