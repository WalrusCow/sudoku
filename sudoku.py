import itertools
import random
import sys

from csp import CSP

class Sudoku(CSP):
    """ Sudoku as a constraint satisfaction problem. """

    def __init__(self):
        super().__init__()
        r = range(3)
        self.variables = set(itertools.product(r, r, r, r))
        self.domain = list(range(1, 10))

    def _check_consistency(self, var):
        br, bc, cr, cc = var
        val = self.assignment[var]
        r = range(3)

        # Check the box for duplicates
        for i, j in itertools.product(r, r):
            key = (br, bc, i, j)
            if key not in self.assignment or key == var:
                continue
            if self.assignment[key] == val:
                return False

        # Check the row for duplicates
        for i, j in itertools.product(r, r):
            key = (br, i, cr, j)
            if key not in self.assignment or key == var:
                continue
            if self.assignment[key] == val:
                return False

        # Check the column for duplicates
        for i, j in itertools.product(r, r):
            key = (i, bc, j, cc)
            if key not in self.assignment or key == var:
                continue
            if self.assignment[key] == val:
                return False

        return True

    def select_unassigned_var(self):
        unassigned = list(self.variables - set(self.assignment))
        return random.choice(unassigned)

    def order_domain_values(self, var):
        # Copy for safety
        l = self.domain[:]
        random.shuffle(l)
        return l

    def __str__(self):
        grid = [['x'] * 9 for _ in range(9)]
        for v in self.variables:
            br, bc, cr, cc = v
            row = 3 * br + cr
            col = 3 * bc + cc
            if v in self.assignment:
                grid[row][col] = self.assignment[v]

        return '\n'.join(' '.join(map(str, row)) for row in grid)

nodes_visited = 0

def csp_backtrack(csp, first=10):
    """ Solve a constraint satisfaction problem `csp` through backtracking. """

    global nodes_visited
    if csp.complete():
        return csp
    var = csp.select_unassigned_var()
    for value in csp.order_domain_values(var):
        #if first: print(value)
        nodes_visited += 1
        if csp.assign(var, value):
            result = csp_backtrack(csp)#, first and first-1)
            if result is not None:
                return result
            csp.unassign(var)
    return None

if __name__ == '__main__':
    csp = Sudoku()
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

    r = csp_backtrack(csp)
    print(r or 'No solution found')
    print(nodes_visited)
