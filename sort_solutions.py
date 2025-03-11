import csv

def sort_key(row):
    """Convert space-separated card values to sortable tuple"""
    return tuple(map(int, row[0].split()))

def main():
    rows = []
    # Read and store header and data
    with open('card_solutions.csv', 'r') as f:
        reader = csv.reader(f)
        header = next(reader)  # Get header
        rows = list(reader)    # Get all data rows
    
    # Sort rows based on card values
    sorted_rows = sorted(rows, key=sort_key)
    
    # Write sorted results back to CSV
    with open('card_solutions_sorted.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(sorted_rows)

if __name__ == '__main__':
    main()
