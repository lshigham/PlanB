from probo.markets import marketdata
from probo.options import vanilla
from probo.engines import naivemc
from probo.engines import blackscholes

def main():
    md = marketdata.MarketData(0.08, 41.0, 0.30, 0.0)
    theCall = vanilla.VanillaCallPayoff(40.0)
    mcEngine = naivemc.NaiveMC(100)
    bsEngine = blackscholes.BlackScholes()

    # Call option with different engines
    option1 = vanilla.VanillaOption(0.25, md, theCall, bsEngine)
    option2 = vanilla.VanillaOption(0.25, md, theCall, mcEngine)

    print("The price of the call option via Black-Scholes is: {}".format(option1.price()))
    print("The price of the call option via Monte Carlo is: {}".format(option2.price()))


    # Put option with different engines
    thePut = vanilla.VanillaPutPayoff(40.0)
    option3 = vanilla.VanillaOption(0.25, md, thePut, bsEngine)
    option4 = vanilla.VanillaOption(0.25, md, thePut, mcEngine)

    print("The price of the put option via Black-Scholes is: {}".format(option3.price()))
    print("The price of the put option via Monte Carlo is: {}".format(option4.price()))


if __name__ == "__main__":
    main()

