from itertools import combinations
from solver import Solver
import csv
from multiprocessing import Pool, cpu_count
import numpy as np

_Cards = 52  # Number of cards in a deck
_NProc = cpu_count()  # Number of CPU cores

def card_value(card):
    """Convert card number (1-52) to actual value (1-13)"""
    return (card - 1) % 13 + 1

def process_combo(combo):
    """Process a single combination - used by multiprocessing"""
    # values = [card_value(card) for card in combo]
    # values.sort()
    values = combo
    solver = Solver(values)
    has_solution = 'Y' if solver.has_solution() else 'N'
    return (' '.join(map(str, values)), has_solution)

def main():
    # Generate all possible 4-card combinations from 52 cards
    cards = range(1, _Cards + 1)  # Full deck
    card_values = [card_value(card) for card in cards]
    unique_combos = set()
    for combo in combinations(card_values, 4):
        sorted_combo = tuple(sorted(combo))
        unique_combos.add(sorted_combo)
    all_combos = unique_combos
    
    # Use 10 processes (as per CPU cores available)
    num_processes = _NProc
    print(f"Using {num_processes} processes")
    
    with Pool(processes=num_processes) as pool:
        # Process combinations in parallel and collect results
        results = set()
        for i, result in enumerate(pool.imap_unordered(process_combo, all_combos, chunksize=100)):
            results.add(result)
            if i % 100 == 0:  # Progress update every 100 combinations
                print(f"Processed {i}/{len(all_combos)} combinations")
    
    # Write results to CSV
    with open('card_solutions.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Cards', 'HasSolution'])  # Header
        writer.writerows(results)

if __name__ == '__main__':
    main()
