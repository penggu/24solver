"""
solver.py
This module contains a Solver class to solve the 24 game
Classes:
    Solver: A class to solve the 24 game.
Functions:
    __init__(self, numbers: list[int], target: int = 24):
    _interleave(self, numbers: list, operators: list) -> list:
    _generate_expressions(self, numbers: list[int], operators: list[str]) -> list[str]:
    _evaluate_expression(self, expression: str) -> float | None:
    _find_solutions_brute_force(self) -> list[str]:
    find_solutions(self) -> list[str]:
        Finds all possible solutions to the 24 game.
    has_solution(self) -> bool:
        Checks if there is at least one solution to the 24 game.
"""

from itertools import permutations, product  # Iteration tools
import ast  # Abstract Syntax Trees
import operator as op  # Operator module

_EPSILON_TOLERANCE = 1e-10  # Small value to account for floating point errors


class Solver:
    """
    A class to solve the 24 game, where the goal is to find a way to
    manipulate 4 numbers so that the end result is 24.
    """

    def __init__(self, numbers: list[int], target: int = 24):
        """
        Constructs a Solver object with a list of numbers.
        """
        self._numbers = numbers
        self._target = target

    def _interleave(self, numbers: list, operators: list) -> list:
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
        for i, operator in enumerate(operators):
            interleaved.append(numbers[i])
            interleaved.append(operator)
        interleaved.append(numbers[-1])
        return interleaved

    def _generate_expressions(
        self, numbers: list[int], operators: list[str]
    ) -> list[str]:
        """
        Generate all possible expressions by interleaving numbers and operators
        and inserting parentheses in different patterns.

        Args:
            numbers (list): A list of numbers to be used in the expressions.
            operators (list): A list of operators to be used in the expressions.

        Returns:
            list: A list of strings, each representing a possible expression.
        """
        expressions = []
        # All possible ways to insert parentheses
        patterns = [
            "(({} {} {}) {} {}) {} {}",  # ((a op b) op c) op d
            "({} {} ({} {} {})) {} {}",  # (a op (b op c)) op d
            "({} {} {}) {} ({} {} {})",  # (a op b) op (c op d)
            "{} {} (({} {} {}) {} {})",  # a op ((b op c) op d)
            "{} {} ({} {} ({} {} {}))",  # a op (b op (c op d))
        ]
        for pattern in patterns:
            # Interleave numbers and operators
            interleaved = self._interleave(numbers, operators)
            expression = pattern.format(*interleaved)
            expressions.append(expression)
        return expressions

    def _evaluate_expression(self, expression: str) -> float | None:
        """
        Evaluates a mathematical expression and returns the result.

        Args:
            expression (str): The mathematical expression to evaluate.

        Returns:
            float: The result of the evaluated expression.
            None: If a ZeroDivisionError occurs during evaluation.
        """
        try:
            # supported operators
            operators = {
                ast.Add: op.add,
                ast.Sub: op.sub,
                ast.Mult: op.mul,
                ast.Div: op.truediv,
            }

            def eval_expr(expr):
                """
                Evaluates a mathematical expression safely using ast.
                """

                def _eval(node):
                    if isinstance(node, ast.Constant):  # <number>
                        return node.value
                    elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
                        return operators[type(node.op)](
                            _eval(node.left), _eval(node.right)
                        )
                    else:
                        raise TypeError(node)

                return _eval(ast.parse(expr, mode="eval").body)

            result = eval_expr(
                expression
            )  # used to be eval(expression) but that is unsafe
            return result
        except ZeroDivisionError:
            return None

    def _find_solutions_brute_force(self) -> list[str]:
        """
        Finds all possible solutions to the 24 game using a brute force approach.
        This method generates all permutations of the given numbers and all combinations
        of the operators ('+', '-', '*', '/'). For each permutation of numbers and each
        combination of operators, it generates all possible expressions and evaluates them
        to check if they are close enough to the target value (24).
        Returns:
            list: A list of unique expressions (as strings) that evaluate to the target value.
        """
        solutions = set()  # Use a set to store unique solutions
        operators = ["+", "-", "*", "/"]
        # Generate all permutations of numbers and operators
        num_permutations = set(
            permutations(self._numbers)
        )  # Use a set to store unique permutations
        op_combinations = set(
            product(operators, repeat=3)
        )  # Use a set to store unique combinations

        for num_perm in num_permutations:
            for op_comb in op_combinations:
                expressions = self._generate_expressions(num_perm, op_comb)
                for expr in expressions:
                    result = self._evaluate_expression(expr)
                    # print(f"Trying: {expr} = {result}")
                    # For rounding errors, check if it is close enough
                    if (result is not None) and abs(
                        result - self._target
                    ) < _EPSILON_TOLERANCE:
                        solutions.add(expr)  # Add to set to ensure uniqueness
        return list(solutions)  # Convert set back to list

    def find_solutions(self) -> list[str]:
        """
        Finds all possible solutions to the 24 solver problem using a brute force approach.

        Returns:
            list[str]: A list of strings, each representing a valid solution.
        """
        return self._find_solutions_brute_force()

    def has_solution(self) -> bool:
        """
        Determines if there is at least one solution.

        Returns:
            bool: True if there is at least one solution, False otherwise.
        """
        return len(self.find_solutions()) > 0
