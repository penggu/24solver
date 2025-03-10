from solver import Solver

# Example usage
if __name__ == '__main__':
    numbers = [5, 5, 5, 1]
    solver = Solver(numbers)
    solutions = solver.find_solutions()
    if solutions:
        print(f"Solutions found: {len(solutions)}")
        for sol in solutions:
            print(sol)
    else:
        print("No solution found.")
