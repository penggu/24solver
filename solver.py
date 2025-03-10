from itertools import permutations, product

class Solver:
    """
    A class to solve the 24 game, where the goal is to find a way to 
    manipulate four numbers so that the end result is 24.

    Attributes:
    ----------
    numbers : list
        A list of four integers to be used in the game.

    Methods:
    -------
    __init__(numbers):
        Initializes the Solver with a list of numbers.
    
    apply_operation(a, b, op):
        Applies a given arithmetic operation to two numbers and returns 
        the result.
    
    interleave(numbers, operators):
        Interleaves a list of numbers with a list of operators.
    
    generate_expressions(numbers, operators):
        Generates all possible expressions by inserting parentheses in 
        different ways.
    
    evaluate_expression(expression):
        Evaluates a given arithmetic expression and returns the result if 
        it is an integer, otherwise returns None.
    
    find_solutions():
        Finds all possible expressions that evaluate to 24 using the given 
        numbers and returns them as a list.
    """
    def __init__(self, numbers):
        self.numbers = numbers

    def apply_operation(self, a, b, op):
        if op == '+':
            return a + b
        elif op == '-':
            return a - b
        elif op == '*':
            return a * b
        elif op == '/':
            if b != 0:
                return a / b
            else:
                return None

    def interleave(self, numbers, operators):
        interleaved = []
        for i in range(len(operators)):
            interleaved.append(numbers[i])
            interleaved.append(operators[i])
        interleaved.append(numbers[-1])
        return interleaved

    def generate_expressions(self, numbers, operators):
        expressions = []
        # All possible ways to insert parentheses
        patterns = [
            '(({} {} {}) {} {}) {} {}',
            '({} {} ({} {} {})) {} {}',
            '({} {} {}) {} ({} {} {})',
            '{} {} (({} {} {}) {} {})',
            '{} {} ({} {} ({} {} {}))'
        ]
        for pattern in patterns:
            # Interleave numbers and operators
            interleaved = self.interleave(numbers, operators)
            expression = pattern.format(*interleaved)
            expressions.append(expression)
        return expressions

    def evaluate_expression(self, expression):
        try:
            result = eval(expression)
            return result if result.is_integer() else None
        except ZeroDivisionError:
            return None

    def find_solutions(self):
        solutions = []
        operators = ['+', '-', '*', '/']
        # Generate all permutations of numbers and operators
        num_permutations = permutations(self.numbers)
        op_combinations = product(operators, repeat=3)
        for num_perm in num_permutations:
            for op_comb in op_combinations:
                expressions = self.generate_expressions(num_perm, op_comb)
                for expr in expressions:
                    if self.evaluate_expression(expr) == 24:
                        solutions.append(expr)
        return solutions

# Example usage
if __name__ == '__main__':
    numbers = [4, 8, 3, 6]
    solver = Solver(numbers)
    solutions = solver.find_solutions()
    if solutions:
        print("Solutions found:")
        for sol in solutions:
            print(sol)
    else:
        print("No solution found.")