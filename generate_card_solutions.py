from itertools import combinations
from solver import Solver
from multiprocessing import Pool, cpu_count
import json
import os.path

_Cards = 52  # Number of cards in a deck
_NProc = cpu_count()  # Number of CPU cores
_SolutionFileName = 'card_solutions.json'

def card_value(card):
    """Convert card number (1-52) to actual value (1-13)"""
    return (card - 1) % 13 + 1

def process_combo(combo):
    """Process a single combination - used by multiprocessing"""
    values = combo
    solver = Solver(values)
    solutions = solver.find_solutions()
    return {
        'cards': ' '.join(map(str, values)),
        'has_solution': len(solutions) > 0,
        'solutions': solutions
    }

def load_existing_solutions():
    """Load existing solutions from JSON file if it exists"""
    if os.path.exists(_SolutionFileName):
        with open(_SolutionFileName, 'r') as f:
            return json.load(f)
    return {}

def main():
    # Try to load existing solutions
    existing_solutions = load_existing_solutions()
    print(f"Loaded {len(existing_solutions)} existing solutions")
    
    # Generate all possible 4-card combinations from 52 cards
    cards = range(1, _Cards + 1)
    card_values = [card_value(card) for card in cards]
    unique_combos = set()
    for combo in combinations(card_values, 4):
        sorted_combo = tuple(sorted(combo))
        unique_combos.add(sorted_combo)
    
    # Filter out combinations we've already solved
    all_combos = [combo for combo in unique_combos 
                 if ' '.join(map(str, combo)) not in existing_solutions]
    print(f"Processing {len(all_combos)} new combinations")
    
    if all_combos:  # Only process if there are new combinations
        num_processes = _NProc
        print(f"Using {num_processes} processes")
        
        with Pool(processes=num_processes) as pool:
            # Process combinations in parallel and collect results
            solutions = {}
            for i, result in enumerate(pool.imap_unordered(process_combo, all_combos, chunksize=100)):
                solutions[result['cards']] = result
                if i % 100 == 0:
                    print(f"Processed {i}/{len(all_combos)} combinations")
        
        # Merge with existing solutions
        existing_solutions.update(solutions)
    
    # Write all results to JSON
    with open(_SolutionFileName, 'w') as f:
        json.dump(existing_solutions, f, indent=2)

if __name__ == '__main__':
    main()
