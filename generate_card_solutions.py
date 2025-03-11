from itertools import combinations
from solver import Solver
from multiprocessing import Pool, cpu_count
import json
import os.path
import csv

_Cards = 52  # Number of cards in a deck
_NProc = cpu_count()  # Number of CPU cores
_SolutionJsonFileName = 'card_solutions.json'
_SolutionCsvFileName = 'card_solutions.csv'

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
    if os.path.exists(_SolutionJsonFileName):
        with open(_SolutionJsonFileName, 'r') as f:
            return json.load(f)
    return {}

def key_to_tuple(key):
    """Convert space-separated string of numbers to tuple"""
    return tuple(map(int, key.split()))

def sort_map_by_key(data: dict):
    """Sort dictionary by key converted to tuple"""
    return dict(sorted(data.items(), key=lambda x: key_to_tuple(x[0])))


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
    
    # Sort solutions by card values
    existing_solutions = sort_map_by_key(existing_solutions)

    # Write all results to JSON
    with open(_SolutionJsonFileName, 'w') as f:
        json.dump(existing_solutions, f, indent=2)

    # Write all results to CSV
    with open(_SolutionCsvFileName, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['cards', 'has_solution', 'solutions'])
        for key, value in existing_solutions.items():
            solutions = json.dumps(value['solutions'])
            solutions = str(value['solutions']).replace(',', ' or')
            writer.writerow([key, value['has_solution'], solutions])

    print(f"Saved {len(existing_solutions)} total solutions")
    
if __name__ == '__main__':
    main()
