# Cool example of a Factory Method Pattern

We can adapt this pattern to do something similar. We can build an abstract pricing engine (market data, etc) ffactory class, and then several concrete factory classes (such as analyic engine, tree engine, monte carlo engine, etc). 

Then we can have option aggregate the factory and have a method to build a pricing engine to get called in it's `price` method. It could also do something similar for `MarketData`.


