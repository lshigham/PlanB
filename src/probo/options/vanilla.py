import abc
import numpy as np
from probo.options.option import Option
from probo.payoffs.payoff import Payoff, PayoffType
from probo.engines.pricingengine import PricingEngine

class VanillaOption(Option):
    def __init__(self, expiry, marketData, payoff, engine):
        if not isinstance(payoff, Payoff):
            raise TypeError("Expected object of type Payoff, got {}.".format(type(payoff).__name__))
        if not isinstance(engine, PricingEngine):
            raise TypeError("Expected object of type PricingEngine, got {}.".format(type(engine).__name__))
        self.__marketData = marketData
        self.__payoff = payoff 
        self.__expiry = expiry
        self.__engine = engine

    @property
    def expiry(self):
        return self.__expiry

    @expiry.setter
    def expiry(self, new_expiry):
        self.__expiry = new_expiry
    
    @property 
    def strike(self):
        return self.__payoff.strike

    @property
    def marketData(self):
        return (self.__marketData.riskFreeRate, self.__marketData.spotPrice, self.__marketData.volatility, self.__marketData.dividendYield)

    @property
    def payoffType(self):
        return self.__payoff.payoffType

    @payoffType.setter
    def payoffType(self, new_payoff_type):
        self.__payoff.payoffType = new_payoff_type

    def payoff(self, spot):
        return self.__payoff.value(spot)

    def price(self):
        return self.__engine.calculate(self)


class VanillaCallPayoff(Payoff):
    def __init__(self, strike):
        self.__strike = strike 
        self.__type = PayoffType.call

    @property
    def strike(self):
        return self.__strike

    @strike.setter
    def strike(self, newStrike):
        self.__strike = newStrike

    @property
    def payoffType(self):
        return self.__type

    def value(self, spot):
        return np.maximum(spot - self.__strike, 0.0)


class VanillaPutPayoff(Payoff):
    def __init__(self, strike):
        self.__strike = strike
        self.__type = PayoffType.put

    @property
    def strike(self):
        return self.__strike

    @strike.setter
    def strike(self, newStrike):
        self.__strike = newStrike

    @property
    def payoffType(self):
        return self.__type

    def value(self, spot):
        return np.maximum(self.__strike - spot, 0.0)


