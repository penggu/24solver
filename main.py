import sys
from solver import Solver

def main():
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
        print("Invalid input. Please enter exactly 4 numbers and optionally a target value.")
        return

    solver = Solver(numbers, target)
    solutions = solver.find_solutions()
    if solutions:
        print(f"Solutions found: {len(solutions)}")
        for sol in solutions:
            print(sol)
    else:
        print("No solution found.")

if __name__ == '__main__':
    main()
