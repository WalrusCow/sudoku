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
        self.possibilities = dict()
        for k in self.variables:
            self.possibilities[k] = set(self.domain)

    def _check_consistency(self, var):
        # How to update after backtrack?
        br, bc, cr, cc = var
        val = self.assignment[var]

        updateKeys = set()
        valSet = {val}

        def checkWithKey(keyGetter):
            r = range(3)
            for i, j in itertools.product(r, r):
                key = keyGetter(i, j)
                if key == var: continue
                if key not in self.assignment:
                    if self.possibilities[key] == valSet:
                        # Check that there remains at least one possibility
                        #print('No more possibilities for {}'.format(key))
                        #print(self)
                        #print(self.possibilities[key])
                        #print(var, val)
                        #input()
                        return False
                    continue
                    updateKeys.add(key)
                elif self.assignment[key] == val:
                    # Check for a conflict
                    return False
            return True

            # Check the box
        if (not checkWithKey(lambda i, j: (br, bc, i, j)) or
            # Check row
            not checkWithKey(lambda i, j: (br, i, cr, j)) or
            # Check the column
            not checkWithKey(lambda i, j: (i, bc, j, cc))):
                return False

        #print(updateKeys)
        #print(self)
        #input()
        for key in updateKeys:
            self.possibilities[key] -= valSet
        self.possibilities[var] = valSet
        return True

    def select_unassigned_var(self):
        unassigned = list(self.variables - set(self.assignment))
        return random.choice(unassigned)

    def order_domain_values(self, var):
        # Copy for safety
        l = self.domain[:]
        random.shuffle(l)
        return l

    def recompute_possibilities(self):
        for k in self.variables:
            self.possibilities[k] = set(self.domain)

        def updatePossibilities(var, val, keyGetter):
            r = range(3)
            valSet = {val}
            for i, j in itertools.product(r, r):
                key = keyGetter(i, j)
                if key == var: continue
                self.possibilities[key] -= valSet

        for key, val in self.assignment.items():
            self.possibilities[key] = {val}
            # Box
            updatePossibilities(key, val, lambda i, j: (br, bc, i, j))
            # Row
            updatePossibilities(key, val, lambda i, j: (br, i, cr, j))
            # Col
            updatePossibilities(key, val, lambda i, j: (i, bc, j, cc))

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
        csp.recompute_possibilities()
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
    with open(sys.argv[1]) as f:
        for i, line in enumerate(map(str.strip, f)):
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
