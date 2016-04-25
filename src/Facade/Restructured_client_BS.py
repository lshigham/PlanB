import payoff 
import pricingEngine

def main():
    strike = 40.0
    expiry = .25 
    
    spot = 41.0
    rate = 0.08
    volatility = 0.30
    dividend = 0.0
    steps = 500 

    call = Vanilla_Payoff(expiry, strike, payoff.black_scholes_call_payoff)
    data = MarketData(rate, spot, volatility, dividend)
    bs_engine = pricingEngine.BlackScholesPricingEngine(steps, pricingEngine.Black_Scholes_Pricer)
    
    the_option = OptionFacade(call, bs_engine, data)
    price = the_option.price()
    print("The Call Price is {0:.3f}".format(price))
    
if __name__ == "__main__":
    main()
