import json

def key_to_tuple(key):
    """Convert space-separated string of numbers to tuple"""
    return tuple(map(int, key.split()))

def main():
    # Read JSON file
    with open('card_solutions.json', 'r') as f:
        data = json.load(f)
    
    # Sort items based on key converted to tuple
    sorted_items = dict(sorted(data.items(), key=lambda x: key_to_tuple(x[0])))
    
    # Write sorted JSON back to file
    with open('card_solutions_sorted.json', 'w') as f:
        json.dump(sorted_items, f, indent=2)

if __name__ == '__main__':
    main()
