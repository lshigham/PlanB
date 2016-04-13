import abc
import Option
from probo.options.option import Option
from probo.payoffs.payoff import payoff, PayoffType

class binomial (Option):
    def __init__(self, payoff, spot, strike):

# Here is the oop portion I need to put into the 
        def Call_binomial_payoff(strike, spot, Option):
            if(Option.payoffType is PayoffType.call):
                return np.maximum(spot - strike, 0.0)
    
        def Put_binomial_payoff(strike, spot, Option):
            if(Option.payoffType is PayoffType.put):
                return np.maximum(strike - spot, 0.0)
                