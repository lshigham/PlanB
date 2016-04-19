import numpy as np

class VanillaOption(object):

    """Base Class for Vanilla Options"""

    def __init__(self, strike, expiry, payoff):
        self.strike = strike
        self.expiry = expiry
        self.payoff = payoff

    def payoff(self, spot):
        return payoff(self, spot)


def call_payoff(name, spot):
    return np.maximum(spot - name.strike, 0.0)

def put_payoff(name, spot):
    return np.maximum(name.strike - spot, 0.0)

## main
call_option = VanillaOption(40.0, 1.0, call_payoff)
put_option = VanillaOption(40.0, 1.0, put_payoff)
spot1 = 42.0
spot2 = 38.0

print("The Call Payoff for a Spot Price of {0} is {1}".format(spot1, call_option.payoff()))
print("The Put Payoff for a Spot Price of {0} is {1}".format(spot2, put_option.payoff()))
