from abc import ABC, abstractmethod

class CSP(ABC):
    """ A constraint satisfaction problem, with assignment. """

    def __init__(self):
        """ Set up a CSP to work with. """
        self.variables = set()
        self.assignment = dict()

    @abstractmethod
    def _check_consistency(self, var):
        """
        Implementation of constraints checking. `var` is the variable update
        that caused this check.
        """
        pass

    @abstractmethod
    def select_unassigned_var(self):
        """ Select an unassigned variable. """
        pass

    @abstractmethod
    def order_domain_values(self, var):
        """ Choose an order to attempt domain values for `var`. """
        pass

    @abstractmethod
    def recompute_possibilities(self):
        """ Re-compute possibilities for each variable. """
        pass

    def assign(self, var, value):
        """
        Attempt to assign a value to a variable. Return whether or
        not the assignment was successful (was valid).
        """
        self.assignment[var] = value
        if self._check_consistency(var):
            return True
        self.unassign(var)
        return False

    def unassign(self, var):
        """ Unassign a variable. """
        del self.assignment[var]

    def complete(self):
        """ Return whether or not this problem is complete. """
        return len(self.assignment) == len(self.variables)
