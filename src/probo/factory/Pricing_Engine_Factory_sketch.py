########## The Factory's base class #########
class Pricing_Engine(object):
  
  def create_pricing_engine_type(self, **args):
    raise NotImplementedError("Requires derived factory class for implementation.")
    

######### The class of the object that needs creating ###########
class Payoff_function(object):
  
  def price(self):
    print ("Doing some things!")
    

######### The  Factory of the class that needs creating ##########
### Multiple different pricing engines can be made here -- analytical, binomial, mc, ect...
class Pricing_Engine_Type(Pricing_Engine):
  
  def create_pricing_engine_type(self):
    return Payoff_function()
    
    
######### The class that needs a product ###########
class Option_Type(object):
  
    def __init__(self, pricing_engine_factory):
      self.pricing_engine_factory = pricing_engine_factory
    
    def option_payoff(self):
      payoff_function = self.pricing_engine_factory.create_pricing_engine_type()
      payoff_function.price()
      
      
######## Start le program #########      
def main():
  pricing_engine_factory = Pricing_Engine_Type()
  Option_type = Option_Type(pricing_engine_factory)
  Option_type.option_payoff()
  
  
  
######## Catch the start of the Program ########
if __name__ == "__main__":
  main()