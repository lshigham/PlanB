import abc


class Option(object, metaclass=abc.ABCMeta):
    """An option.

    The doc string.
    """

    @property
    @abc.abstractmethod
    def expiry(self):
        """Get the expiry date."""

    @expiry.setter
    @abc.abstractmethod
    def expiry(self, newExpiry):
        """Set the expiry date."""
    
    @abc.abstractmethod
    def payoff(self):
        """Get the option's payoff value."""


