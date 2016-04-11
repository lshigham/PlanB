import abc
import enum


class Payoff(object, metaclass=abc.ABCMeta):
    
    @abc.abstractmethod
    def value(self):
        pass


class PayoffType(enum.Enum):
    call = 0
    put = 1
