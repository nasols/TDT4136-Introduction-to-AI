# CSP Assignment
# Original code by Håkon Måløy
# Updated by Xavier Sánchez Díaz

import copy
from itertools import product as prod
import string
import sys
import random
import time


start = time.time()

class CSP:
    def __init__(self):
        # self.variables is a list of the variable names in the CSP
        self.variables = []

        # self.domains is a dictionary of domains (lists)
        self.domains = {}

        # self.constraints[i][j] is a list of legal value pairs for
        # the variable pair (i, j)
        self.constraints = {}

        self.backtracks = 0
        self.failed = 0
        self.domainSum = 0 

    def add_variable(self, name: str, domain: list):
        """Add a new variable to the CSP.

        Parameters
        ----------
        name : str
            The name of the variable to add
        domain : list
            A list of the legal values for the variable
        """
        self.variables.append(name)
        self.domains[name] = list(domain)
        self.constraints[name] = {}

    def get_all_possible_pairs(self, a: list, b: list) -> list[tuple]:
        """Get a list of all possible pairs (as tuples) of the values in
        lists 'a' and 'b', where the first component comes from list
        'a' and the second component comes from list 'b'.

        Parameters
        ----------
        a : list
            First list of values
        b : list
            Second list of values

        Returns
        -------
        list[tuple]
            List of tuples in the form (a, b)
        """
        return prod(a, b)

    def get_all_arcs(self) -> list[tuple]:
        """Get a list of all arcs/constraints that have been defined in
        the CSP.

        Returns
        -------
        list[tuple]
            A list of tuples in the form (i, j), which represent a
            constraint between variable `i` and `j`
        """
        return [(i, j) for i in self.constraints for j in self.constraints[i]]

    def get_all_neighboring_arcs(self, var: str) -> list[tuple]:
        """Get a list of all arcs/constraints going to/from variable 'var'.

        Parameters
        ----------
        var : str
            Name of the variable

        Returns
        -------
        list[tuple]
            A list of all arcs/constraints in which `var` is involved
        """
        return [(i, var) for i in self.constraints[var]]

    def add_constraint_one_way(self, i: str, j: str,
                               filter_function: callable):
        """Add a new constraint between variables 'i' and 'j'. Legal
        values are specified by supplying a function 'filter_function',
        that should return True for legal value pairs, and False for
        illegal value pairs.

        NB! This method only adds the constraint one way, from i -> j.
        You must ensure to call the function the other way around, in
        order to add the constraint the from j -> i, as all constraints
        are supposed to be two-way connections!

        Parameters
        ----------
        i : str
            Name of the first variable
        j : str
            Name of the second variable
        filter_function : callable
            A callable (function name) that needs to return a boolean.
            This will filter value pairs which pass the condition and
            keep away those that don't pass your filter.
        """
        if j not in self.constraints[i]:
            # First, get a list of all possible pairs of values
            # between variables i and j
            self.constraints[i][j] = self.get_all_possible_pairs(
                                        self.domains[i],
                                        self.domains[j])

        # Next, filter this list of value pairs through the function
        # 'filter_function', so that only the legal value pairs remain
        self.constraints[i][j] = list(filter(lambda
                                             value_pair:
                                             filter_function(*value_pair),
                                             self.constraints[i][j]))

    def add_all_different_constraint(self, var_list: list):
        """Add an Alldiff constraint between all of the variables in the
        list provided.

        Parameters
        ----------
        var_list : list
            A list of variable names
        """
        for (i, j) in self.get_all_possible_pairs(var_list, var_list):
            if i != j:
                self.add_constraint_one_way(i, j, lambda x, y: x != y)

    def backtracking_search(self):
        """This functions starts the CSP solver and returns the found
        solution.
        """
        
        # Make a so-called "deep copy" of the dictionary containing the
        # domains of the CSP variables. The deep copy is required to
        # ensure that any changes made to 'assignment' does not have any
        # side effects elsewhere.
        assignment = copy.deepcopy(self.domains)

        # Run AC-3 on all constraints in the CSP, to weed out all of the
        # values that are not arc-consistent to begin with
        self.inference(assignment, self.get_all_arcs())



        # Call backtrack with the partial assignment 'assignment'
        return self.backtrack(assignment)

    # Edited method, see internal comments inside the method definition
    def backtrack(self, assignment):
        """The function 'Backtrack' from the pseudocode in the
        textbook.

        The function is called recursively, with a partial assignment of
        values 'assignment'. 'assignment' is a dictionary that contains
        a list of all legal values for the variables that have *not* yet
        been decided, and a list of only a single value for the
        variables that *have* been decided.

        When all of the variables in 'assignment' have lists of length
        one, i.e. when all variables have been assigned a value, the
        function should return 'assignment'. Otherwise, the search
        should continue. When the function 'inference' is called to run
        the AC-3 algorithm, the lists of legal values in 'assignment'
        should get reduced as AC-3 discovers illegal values.

        IMPORTANT: For every iteration of the for-loop in the
        pseudocode, you need to make a deep copy of 'assignment' into a
        new variable before changing it. Every iteration of the for-loop
        should have a clean slate and not see any traces of the old
        assignments and inferences that took place in previous
        iterations of the loop.
        """        

        # First we define a boolean that is initiated as true
        finished = True

        # Then we get all the variables from assignment, and check if the length is greater than 1.
        # If all of the variables have length 1, that means all of the variables have been assigned a value and the sudoku should be solved
        # However, if any one variable does have length greater than 1, then the sudoku is not solved so finished is set to false
        for key, variable in assignment.items():
            if not len(variable) == 1:
                finished = False
        if finished:
            return assignment

        # For every time we go through the backtracking method, we add one to the backtracks
        self.backtracks = self.backtracks + 1


        # Here we fetch the unassigned variables in assignment i.e variables with length of greater than 1
        variable = self.select_unassigned_random_variable(assignment)
        # Then we go through all of these variables and check all of their values, meaning possible assignments
        for value in assignment[variable]:
            # Here we make a deepcopy of the assignment and assign the current variable the current value
            assCopy = copy.deepcopy(assignment)
            assCopy[variable] = value
            # AC-3
            # Here we call the inference method on the copy of the assignment,
            # And then we recursively backtrack if the inference method returns true
            inferences = self.inference(assCopy, self.get_all_arcs())
            if inferences:
                result = self.backtrack(assCopy)
                # If this yields a result, then we return this result,
                # if not, then we increase the counter for every failed back track and return nothing
                if result:
                    return result
        self.failed = self.failed + 1
        return None
        
    # Edited method, see internal comments inside the method definition
    def select_unassigned_variable(self, assignment):
        """The function 'Select-Unassigned-Variable' from the pseudocode
        in the textbook. Should return the name of one of the variables
        in 'assignment' that have not yet been decided, i.e. whose list
        of legal values has a length greater than one.
        """
        ## First we get the keys from the assignment
        #  Then we check every key and return all of the keys that have not yet been assigned a value
        keys = assignment.keys()
        for key in keys: 
            # If the length of the key is greater than 1, then that key has yet to decide a final variable
            # It is therefore returned so that it can be assigned a variable
            if len(assignment.get(key)) > 1 : 
                var = key
                #self.domainSum += len(assignment[var])
                return var
    
    def select_unassigned_random_variable(self, assignment) : 

        
        rand1 = random.randint(0, 8)
        rand2 = random.randint(0, 8)

        var = str(rand1)+"-"+str(rand2)

        #self.domainSum += len(assignment[var])


        return var 

    def select_unassigned_highest_domain_size_variable(self, assignment) : 

        keys = assignment.keys()
        var = self.select_unassigned_variable(assignment) # selects random unassigned value

        for key in keys: 
            if len(assignment[key]) >= len(assignment[var]): 
                var = key
                #self.domainSum += len(assignment[var])
        
        return var
    
    def select_unassigned_lowest_domain_size_variable(self, assignment) : 

        keys = assignment.keys()
        var = self.select_unassigned_variable(assignment) # selects unassigned value with domain bigger than 1

        for key in keys: 
            if (len(assignment[key]) > 1) and (len(assignment[key]) <= len(assignment[var])) : 
                var = key
                self.domainSum += len(assignment[var])
        

        return var


     
    # Edited method, see internal comments inside the method definition
    def inference(self, assignment, queue):
        """The function 'AC-3' from the pseudocode in the textbook.
        'assignment' is the current partial assignment, that contains
        the lists of legal values for each undecided variable. 'queue'
        is the initial queue of arcs that should be visited.
        """
    
        # Debugging stuff
        """
        #queue = queue
        print("01: ", assignment.get("0-1"))
        print("02: ", assignment.get("0-2")) 
        """

        ## In this method we check through the queue of the partial assignment "assignment"
        #  While there still is a queue, we pop from the queue
        #  Then we call the revise method, and if that returns true,
        #  meaning it has removed an illegal value, then we check if the length of the queue is 0
        #  if so, we return false, if not, we continue.
        #  then we get all the arc's from the neighbours and remove the neighbour if its has the same value
        #  and finally we insert the neighbours in the queue
        #  once this is all done, we return True back to the backtracking algorithm
        while queue:

            (i, j) = queue.pop()          

            if self.revise(assignment, i, j): 
                if len(assignment.get(i)) == 0 : 
                    return False
                
                neighbors = self.get_all_neighboring_arcs(i) 

                for neighbor in neighbors : 
                    if neighbor[0] == j: 
                       neighbors.remove(neighbor)
                
                for neighbor in neighbors:
                    queue.insert(0, neighbor)

        return True

        
    # Edited method, see internal comments inside the method definition
    def revise(self, assignment, i, j):
        """The function 'Revise' from the pseudocode in the textbook.
        'assignment' is the current partial assignment, that contains
        the lists of legal values for each undecided variable. 'i' and
        'j' specifies the arc that should be visited. If a value is
        found in variable i's domain that doesn't satisfy the constraint
        between i and j, the value should be deleted from i's list of
        legal values in 'assignment'.
        """

        ## First we initiate revised as false
        revised = False

        ## Then we go through the partial assignment "assignment"
        #  And we remove any of the assignments that don't fit the constraint between
        #  j and i from i. If we have removed a value, then revised will be true and we return revised.
        if len(assignment.get(j)) == 1: 
            if assignment.get(j)[0] in assignment.get(i): 
                assignment.get(i).remove(assignment.get(j)[0])
                revised = True
        return revised


def create_map_coloring_csp():
    """Instantiate a CSP representing the map coloring problem from the
    textbook. This can be useful for testing your CSP solver as you
    develop your code.
    """
    csp = CSP()
    states = ['WA', 'NT', 'Q', 'NSW', 'V', 'SA', 'T']
    edges = {'SA': ['WA', 'NT', 'Q', 'NSW', 'V'],
             'NT': ['WA', 'Q'], 'NSW': ['Q', 'V']}
    colors = ['red', 'green', 'blue']
    for state in states:
        csp.add_variable(state, colors)
    for state, other_states in edges.items():
        for other_state in other_states:
            csp.add_constraint_one_way(state, other_state, lambda i, j: i != j)
            csp.add_constraint_one_way(other_state, state, lambda i, j: i != j)
    return csp


def create_sudoku_csp(filename: str) -> CSP:
    """Instantiate a CSP representing the Sudoku board found in the text
    file named 'filename' in the current directory.

    Parameters
    ----------
    filename : str
        Filename of the Sudoku board to solve

    Returns
    -------
    CSP
        A CSP instance
    """
    csp = CSP()
    board = list(map(lambda x: x.strip(), open(filename, 'r')))

    for row in range(9):
        for col in range(9):
            if board[row][col] == '0':
                csp.add_variable('%d-%d' % (row, col), list(map(str,
                                                                range(1, 10))))
            else:
                csp.add_variable('%d-%d' % (row, col), [board[row][col]])

    for row in range(9):
        csp.add_all_different_constraint(['%d-%d' % (row, col)
                                          for col in range(9)])
    for col in range(9):
        csp.add_all_different_constraint(['%d-%d' % (row, col)
                                         for row in range(9)])
    for box_row in range(3):
        for box_col in range(3):
            cells = []
            for row in range(box_row * 3, (box_row + 1) * 3):
                for col in range(box_col * 3, (box_col + 1) * 3):
                    cells.append('%d-%d' % (row, col))
            csp.add_all_different_constraint(cells)

    return csp


def print_sudoku_solution(solution):
    """Convert the representation of a Sudoku solution as returned from
    the method CSP.backtracking_search(), into a human readable
    representation.
    """
    for row in range(9):
        for col in range(9):
            print(solution['%d-%d' % (row, col)][0], end=" "),
            if col == 2 or col == 5:
                print('|', end=" "),
        print("")
        if row == 2 or row == 5:
            print('------+-------+------')




""" print("veryhard")
sudoku = create_sudoku_csp("veryhard.txt")
#print(sudoku.get_all_neighboring_arcs("0-0"))
#print(sudoku.inference(sudoku, sudoku.get_all_arcs()))

sol = sudoku.backtracking_search()
print_sudoku_solution(sol)  """


# Solving and printing the different sudoku boards
print("\n----------------------------------------------------------------")
print("Easy board: ")
sudokuEasy = create_sudoku_csp("csp_code_handout/easy.txt")
sol1 = sudokuEasy.backtracking_search()
print_sudoku_solution(sol1) 
print("number of failed atempts: ", sudokuEasy.failed)
print("number of backtracks: ", sudokuEasy.backtracks)
print("----------------------------------------------------------------\n")

print("\n----------------------------------------------------------------")
print("Medium board: ")
sudokuMed = create_sudoku_csp("csp_code_handout/medium.txt")
sol2 = sudokuMed.backtracking_search()
print_sudoku_solution(sol2) 
print("number of failed atempts: ", sudokuMed.failed)
print("number of backtracks: ", sudokuMed.backtracks)
print("sum of domain sizes: ", sudokuMed.domainSum)
print("----------------------------------------------------------------\n")

print("\n----------------------------------------------------------------")
print("Hard board: ")
sudokuHard = create_sudoku_csp("csp_code_handout/hard.txt")
sol3 = sudokuHard.backtracking_search()
print_sudoku_solution(sol3) 
print("number of failed atempts: ", sudokuHard.failed)
print("number of backtracks: ", sudokuHard.backtracks)
print("number of domain sizes: ", sudokuHard.domainSum)
print("----------------------------------------------------------------\n")

print("\n----------------------------------------------------------------")
print("Very hard board: ")
sudokuVeryHard = create_sudoku_csp("csp_code_handout/veryhard.txt")
sol4 = sudokuVeryHard.backtracking_search()
print_sudoku_solution(sol4) 
print("number of failed atempts: ", sudokuVeryHard.failed)
print("number of backtracks: ", sudokuVeryHard.backtracks)
print("sum of domain sizes: ", sudokuVeryHard.domainSum)
print("----------------------------------------------------------------\n")


# medEnd = time.time()
# sudokuMed = create_sudoku_csp("/Users/jonasolsen/Documents/Skole/IIkt/3_Semester/Introduksjon_til_kunstig_intelligens/Øvinger/kunstig_repo/csp_code_handout/medium.txt")
# sol2 = sudokuMed.backtracking_search()

# print(medEnd - start)
# print("sum of domain sizes: ", sudokuMed.domainSum)


# vhEnd = time.time()
# sudokuVeryHard = create_sudoku_csp("veryhard.txt")
# sol4 = sudokuVeryHard.backtracking_search()
# print("sum of domain sizes: ", sudokuVeryHard.domainSum)

# print((vhEnd - start))




















