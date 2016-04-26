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

    call = VanillaOption(expiry, strike, payoff.monte_carlo_call_payoff)
    data = MarketData(rate, spot, volatility, dividend)
    mc_engine = pricingEngine.MonteCarloPricingEngine(steps, pricingEngine.Stratified_Monte_Carlo_Pricer)
    
    the_option = OptionFacade(call, mc_engine, data)
    price = the_option.price()
    print("The Call Price is {0:.3f}".format(price))
    
if __name__ == "__main__":
    main()
