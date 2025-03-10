from itertools import permutations, product

_Epsilon = 1e-10 # Small value to account for floating point errors

class Solver:
    """
    A class to solve the 24 game, where the goal is to find a way to 
    manipulate four numbers so that the end result is 24.

    Attributes:
    ----------
    numbers : list
        A list of four integers to be used in the game.
    """

    def __init__(self, numbers: list[int], target: int = 24):
        """
        Constructs a Solver object with a list of numbers.
        """
        self._numbers = numbers
        self._target = target


    def _interleave(self, numbers, operators):
        """
        Interleaves a list of numbers and a list of operators.

        Args:
            numbers (list): A list of numbers to be interleaved.
            operators (list): A list of operators to be interleaved with the numbers.

        Returns:
            list: A new list where the numbers and operators are interleaved.
                  The last number in the numbers list is appended at the end.
        """
        interleaved = []
        for i in range(len(operators)):
            interleaved.append(numbers[i])
            interleaved.append(operators[i])
        interleaved.append(numbers[-1])
        return interleaved

    def _generate_expressions(self, numbers, operators):
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
            interleaved = self._interleave(numbers, operators)
            expression = pattern.format(*interleaved)
            expressions.append(expression)
        return expressions

    def _evaluate_expression(self, expression):
        try:
            result = eval(expression)
            return result
        except ZeroDivisionError:
            return None

    def _find_solutions_brute_force(self):
        solutions = []
        operators = ['+', '-', '*', '/']
        # Generate all permutations of numbers and operators
        num_permutations = permutations(self._numbers)
    
        for num_perm in num_permutations:
            # Need to re-gen every time because op_combinations is an iterator
            op_combinations = product(operators, repeat=3)
            for op_comb in op_combinations:
                expressions = self._generate_expressions(num_perm, op_comb)
                for expr in expressions:
                    result = self._evaluate_expression(expr)
                    # For rounding errors, check if it is close enough
                    if (result is not None) and abs(result - self._target) < _Epsilon:
                        solutions.append(expr)
        return solutions
    
    def find_solutions(self):
        return self._find_solutions_brute_force()

    def has_solution(self):
        return len(self.find_solutions()) > 0
