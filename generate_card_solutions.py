"""
Generate and store solutions for the 24 game using different card combinations.
This module processes all possible 4-card combinations from a standard deck
and finds solutions where the cards can be used to make 24.
"""

import csv
import json
import os.path
from itertools import combinations
from multiprocessing import Pool, cpu_count

from solver import Solver

_N_CARDS = 52  # Number of cards in a deck
_N_PROCS = cpu_count()  # Number of CPU cores
_SOLUTION_JSON_FILE = "card_solutions.json"
_SOLUTION_CSV_FILE = "card_solutions.csv"


def card_value(card):
    """Convert card number (1-52) to actual value (1-13)"""
    return (card - 1) % 13 + 1


def process_combo(combo):
    """Process a single combination - used by multiprocessing"""
    values = combo
    solver = Solver(values)
    solutions = solver.find_solutions()
    return {
        "cards": " ".join(map(str, values)),
        "has_solution": "Y" if len(solutions) > 0 else "N",
        "num_solutions": len(solutions),
        "solutions": solutions,
    }


def load_existing_solutions():
    """Load existing solutions from JSON file if it exists"""
    if os.path.exists(_SOLUTION_JSON_FILE):
        with open(_SOLUTION_JSON_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def key_to_tuple(key):
    """Convert space-separated string of numbers to tuple"""
    return tuple(map(int, key.split()))


def sort_map_by_key(data: dict):
    """Sort dictionary by key converted to tuple"""
    return dict(sorted(data.items(), key=lambda x: key_to_tuple(x[0])))


def main() -> None:
    """
    Generate and store solutions for the 24 game using different card combinations.
    This module processes all possible 4-card combinations from a standard deck
    and finds solutions where the cards can be used to make 24.
    """
    # Try to load existing solutions
    existing_solutions = load_existing_solutions()
    print(f"Loaded {len(existing_solutions)} existing solutions: {_SOLUTION_JSON_FILE}")

    # Generate all possible 4-card combinations from 52 cards
    cards = range(1, _N_CARDS + 1)
    card_values = [card_value(card) for card in cards]
    unique_combos = set()
    for combo in combinations(card_values, 4):
        sorted_combo = tuple(sorted(combo))
        unique_combos.add(sorted_combo)

    # Filter out combinations we've already solved
    all_combos = [
        combo
        for combo in unique_combos
        if " ".join(map(str, combo)) not in existing_solutions
    ]
    print(f"Processing {len(all_combos)} new combinations")

    if all_combos:  # Only process if there are new combinations
        print(f"Using {_N_PROCS} processes")
        with Pool(processes=_N_PROCS) as p:
            # Process combinations in parallel and collect results
            solutions = {}
            for i, result in enumerate(
                p.imap_unordered(process_combo, all_combos, chunksize=100)
            ):
                solutions[result["cards"]] = result
                if i % 100 == 0:
                    print(f"Processed {i}/{len(all_combos)} combinations")

        # Merge with existing solutions
        existing_solutions.update(solutions)

    # Sort solutions by card values
    existing_solutions = sort_map_by_key(existing_solutions)

    # Write all results to JSON
    with open(_SOLUTION_JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(existing_solutions, f, indent=2)

    # Write all results to CSV
    with open(_SOLUTION_CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["cards", "has_solution", "num_solutions"])
        for key, value in existing_solutions.items():
            # solutions = str(value['solutions']).replace(',', ' or')
            writer.writerow([key, value["has_solution"], value["num_solutions"]])

    print(
        f"Saved {len(existing_solutions)} total solutions: "
        f"{_SOLUTION_JSON_FILE}, {_SOLUTION_CSV_FILE}"
    )


if __name__ == "__main__":
    main()
