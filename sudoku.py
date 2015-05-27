import itertools
import sys

from abc import ABC, abstractmethod

class CSP(ABC):
    """ A constraint satisfaction problem, with assignment. """

    def __init__(self):
        """ Set up a CSP to work with. """
        self.variables = set()
        self.assignment = dict()

    @abstractmethod
    def _is_consistent(self):
        """ Implementation of constraints. """
        pass

    @abstractmethod
    def select_unassigned_var(self):
        """ Select an unassigned variable. """
        pass

    @abstractmethod
    def order_domain_values(self, var):
        """ Choose an order to attempt domain values for `var`. """
        pass

    def assign(self, var, value):
        """
        Attempt to assign a value to a variable. Return whether or
        not the assignment was successful (was valid).
        """
        self.assignment[var] = value
        if self._is_consistent():
            return True
        self.unassign(var)
        return False

    def unassign(self, var):
        """ Unassign a variable. """
        del self.assignment[var]

    def complete(self):
        """ Return whether or not this problem is complete. """
        return len(self.assignment) == len(self.variables)


class Sudoku(CSP):
    """ Sudoku as a constraint satisfaction problem. """

    def __init__(self):
        super().__init__()
        print(self.assignment)
        r = range(3)
        self.variables = set(itertools.product(r, r, r, r))

    def _is_consistent(self):
        #print('hello')
        return True

    def select_unassigned_var(self):
        unassigned = self.variables - set(self.assignment)
        # TODO
        return next(unassigned.__iter__())

    def order_domain_values(self, var):
        return list(range(1, 10))

    def __str__(self):
        grid = [['x'] * 9 for _ in range(9)]
        for v in self.variables:
            br, bc, cr, cc = v
            row = 3 * br + cr
            col = 3 * bc + cc
            if v in self.assignment:
                grid[row][col] = self.assignment[v]

        return '\n'.join(' '.join(map(str, row)) for row in grid)


def csp_backtrack(csp):
    """ Solve a constraint satisfaction problem `csp` through backtracking. """

    if csp.complete():
        return csp
    var = csp.select_unassigned_var()
    for value in csp.order_domain_values(var):
        if csp.assign(var, value):
            result = csp_backtrack(csp)
            if result is not None:
                return result
            csp.unassign(var, value)
    return None

if __name__ == '__main__':
    csp = Sudoku()
    print(csp)
    # Read in a sudoku
    for i, line in enumerate(map(str.strip, sys.stdin)):
        for j, val in enumerate(line.split()):
            try:
                val = int(val)
            except ValueError:
                continue
            # Index in line, value
            br = i // 3
            bc = j // 3
            cr = i % 3
            cc = j % 3
            csp.assign((br, bc, cr, cc), val)
    print(csp)

    r = csp_backtrack(csp)
    print(r)
