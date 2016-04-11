class MarketData(object):
    """A class to encapsulate market data variables.

       Especially to be passed to pricing engines.
    """

    def __init__(self, riskFreeRate, spotPrice, volatility, dividendYield):
        self.__riskFreeRate = riskFreeRate
        self.__spotPrice = spotPrice
        self.__volatility = volatility
        self.__dividendYield = dividendYield

    @property
    def riskFreeRate(self):
        return self.__riskFreeRate

    @riskFreeRate.setter
    def riskFreeRate(self, newRate):
        self.__riskFreeRate = newRate

    @property
    def spotPrice(self):
        return self.__spotPrice

    @spotPrice.setter
    def spotPrice(self, newPrice):
        self.__spotPrice = newPrice

    @property
    def volatility(self):
        return self.__volatility

    @volatility.setter
    def volatility(self, newVolatility):
        self.__volatility = newVolatility

    @property
    def dividendYield(self):
        return self.__dividendYield

    @dividendYield.setter
    def dividendYield(self, newYield):
        self.__dividendYield = newYield

