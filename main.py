"""Entry point for the 24 solver program.
This script takes 4 numbers and an optional target value as command line arguments
and finds mathematical expressions using basic operations (+, -, *, /) that
evaluate to the target value (default 24) using all the input numbers exactly once.
Usage:
    python main.py num1 num2 num3 num4 [target]
Arguments:
    num1, num2, num3, num4: Four integer numbers to use in the expression
    target: Optional target value (defaults to 24)
Example:
    python main.py 5 5 5 1 24
Returns:
    Prints all valid solutions found, or "No solution found" if none exist.
"""

import sys
from solver import Solver


def main():
    """Main function for the 24 solver program.
    This function processes command line arguments to solve arithmetic expressions.
    It accepts 4 numbers and an optional target value (defaults to 24).
    Usage:
        python main.py num1 num2 num3 num4 [target]
    Example:
        python main.py 5 5 5 1 24
    Args:
        Command line arguments expected:
            - Four integers representing the numbers to use
            - Optional fifth integer representing the target sum (defaults to 24)
    Returns:
        None. Prints solutions or error messages to stdout.
    The function will:
    1. Validate input arguments
    2. Create a Solver instance with the given numbers and target
    3. Find and display all possible solutions
    4. Print error message if no solutions are found
    """
    if len(sys.argv) <= 1:
        print("Usage: python main.py num1 num2 num3 num4 [target]")
        print("Example: python main.py 5 5 5 1 24")
        return

    # Get numbers and target from command line arguments
    inputs = list(map(int, sys.argv[1:]))

    if len(inputs) == 4:
        numbers = inputs
        target = 24
    elif len(inputs) == 5:
        numbers = inputs[:4]
        target = inputs[4]
    else:
        print(
            "Invalid input. Please enter exactly 4 numbers and optionally a target value."
        )
        return

    solver = Solver(numbers, target)
    solutions = solver.find_solutions()
    if solutions:
        print(f"Solutions found: {len(solutions)}")
        for sol in solutions:
            print(sol)
    else:
        print("No solution found.")


if __name__ == "__main__":
    main()
