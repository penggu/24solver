from itertools import permutations, product

def apply_operation(a, b, op):
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

def interleave(numbers, operators):
    interleaved = []
    for i in range(len(operators)):
        interleaved.append(numbers[i])
        interleaved.append(operators[i])
    interleaved.append(numbers[-1])
    return interleaved

def generate_expressions(numbers, operators):
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
        interleaved = interleave(numbers, operators)
        expression = pattern.format(*interleaved)
        expressions.append(expression)
    return expressions

def evaluate_expression(expression):
    try:
        result = eval(expression)
        return result if result.is_integer() else None
    except ZeroDivisionError:
        return None

def find_solutions(numbers):
    solutions = []
    operators = ['+', '-', '*', '/']
    # Generate all permutations of numbers and operators
    num_permutations = permutations(numbers)
    op_combinations = product(operators, repeat=3)
    for num_perm in num_permutations:
        for op_comb in op_combinations:
            expressions = generate_expressions(num_perm, op_comb)
            for expr in expressions:
                if evaluate_expression(expr) == 24:
                    solutions.append(expr)
    return solutions


# Example usage
if __name__ == '__main__':
    numbers = [4, 8, 3, 6]
    solutions = find_solutions(numbers)
    if solutions:
        print("Solutions found:")
        for sol in solutions:
            print(sol)
    else:
        print("No solution found.")