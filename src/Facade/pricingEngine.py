import abc
import numpy as np
from scipy.stats import binom
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
    disc = np.exp(-rate * expiry)
    discount_rate = np.exp(-rate * delta_t)
    spot_T = 0.0
    down_states = d**range(steps, -1, -1)
    up_states = u ** range(0, steps + 1)
    payoffs = 0.0
    
    
    for i in range(steps, 0, -1):
        spot_i = spot * (u ** (steps - i)) * (d ** (i))
        payoffs += option.payoff(spot_i) * binom.pmf(steps - i, steps, pu)
    price = discount_rate * payoffs     
    
    return price
    # CH18
        
#
# Implements binomial method for an American put.
#from numpy import *
###### Problem and method parameters #########
#S = 3.; E = 4.; #T = 1.;# r = 0.05; #sigma = 0.3
#M = 400; dt = T/M; p =0.5 
#u = exp(sigma*sqrt(dt) + (r-0.5*sigma**2)*dt)
#d = exp(-sigma*sqrt(dt) + (r-0.5*sigma**2)*dt)
#print 'S, E, T, r, sigma=',S, E, T, r, sigma
#print 'M, dt, p=',M, dt,p
#print 'u, d=',u,d
##################################

# Initial computations
#dpowers = d**range(M,-1,-1)
#upowers = u**range(0,M+1)
#W = maximum(E-S*dpowers*upowers,0)
#print 'W=',W
# Work back to option value at time zero
#for i in range(M,0,-1):  # i=M, M-1, .., 1#
#    di=dpowers[M-i+1:M+1]
#    ui=upowers[0:i]
#    Si = S*di*ui
#    W = maximum(maximum(E-Si,0),exp(-r*dt)*(p*W[1:i+1]+(1-p)*W[0:i]))
#print 'Option value is',W



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
    d2 = d1 - sigma * np.sqrt(expiry)

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
    expiry = option.expriy
    strike = option.strike
    (spot, rate, volatility, dividend) = data.get_data()
    discount_rate = np.exp(rate * expiry)
    delta_t = expiry
    z = np.random.normal(size=self.__steps)
    
    nudt = (rate - 0.5 * volatility * volatility) * delta_t
    sidt = volatility * np.sqrt(delta_t)
    
    spot_t = np.zeros((self.__steps, ))
    payoff_t = np.zeros((self.__steps, ))
    spot_t = spot * np.exp(nudt + sidt * z)
    payoff_t = option.payoff(spot_t)
    price = discount_rate * payoff_t.mean()
    
    return price