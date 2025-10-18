import requests
import json
import sys
import os
import time

API_URL = "https://sudoku-api.vercel.app/api/dosuku"
BATCH_LIMIT = 20  # API max per request
MAX_RETRY = 3

def fetch_sudoku_batch(batch_size: int):
    query = f"""{{newboard(limit:{batch_size}){{grids{{value,solution,difficulty}}}}}}"""
    params = {"query": query}

    for attempt in range(MAX_RETRY):
        try:
            response = requests.get(API_URL, params=params, timeout=15)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"Warning: API returned {response.status_code}, retrying...")
        except requests.exceptions.RequestException as e:
            print(f"Warning: Request failed ({e}), retrying...")
        time.sleep(2 ** attempt)  # exponential backoff
    raise RuntimeError(f"Failed to fetch batch of {batch_size} sudokus after {MAX_RETRY} attempts")

def main(args: list[str]):
    if len(args) < 2 or args[1] in ("--help", "help", "-h"):
        print("Usage: get-sudokus.py <quantity>")
        return

    try:
        quantity = int(args[1])
        if quantity <= 0:
            raise ValueError
    except ValueError:
        print("The argument passed is invalid")
        return

    os.makedirs("./assets", exist_ok=True)
    all_grids = []

    for start in range(0, quantity, BATCH_LIMIT):
        batch_size = min(BATCH_LIMIT, quantity - start)
        print(f"Fetching {batch_size} sudokus (batch {start // BATCH_LIMIT + 1})...")
        grids = fetch_sudoku_batch(batch_size)["newboard"]["grids"]
        all_grids.extend(grids)

    file_path = "./assets/sudokus.json"
    with open(file_path, "w") as f:
        json.dump(all_grids, f, indent=2)

    print(f"Saved {len(all_grids)} sudokus to {file_path}")

if __name__ == "__main__":
    main(sys.argv)
