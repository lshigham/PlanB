import payoff 
import pricingEngine


def main():
    strike = 40.0
    expiry = 1.0 
    
    spot = 41.0
    rate = 0.08
    volatility = 0.30
    dividend = 0.0
    steps = 3 

    put = Vanilla_Payoff(expiry, strike, payoff.put_payoff)
    data = MarketData(rate, spot, volatility, dividend)
    binom_engine = pricingEngine.BinomialPricingEngine(steps, pricingEngine.AmericanBinomialPricer)
    
    the_option = OptionFacade(put, binom_engine, data)
    price = the_option.price()
    print("The put price is {0:.3f}".format(price))
    
if __name__ == "__main__":
    main()

