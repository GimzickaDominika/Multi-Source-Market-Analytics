import requests
import csv
import time
import sys
API_KEY = 'token'
OUTPUT_FILE = 'fundamental_data.csv'

raw_symbols = [
    'AAPL', 
    'AMZN', 
    'NVDA', 
    'BRK.B', 
    'INTC', 
    'AMD'
]

def clean_symbol(sym):
    """
    Cleans the symbol format for Alpha Vantage API.
    Removes exchange prefixes and converts dots to hyphens (e.g., BRK.B -> BRK-B).
    """
    if ':' in sym:
        return sym.split(':')[-1] 
    return sym.replace('.', '-') 

def main():
    processed_symbols = [clean_symbol(s) for s in raw_symbols]
    successful_data = []

    print(f"Processing symbols: {processed_symbols}")
    for symbol in processed_symbols:
        try:
            url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={API_KEY}'
            r = requests.get(url)
            data = r.json()
            if not data:
                print(f"SKIPPED: {symbol} (No fundamental data available or not a stock).")
                continue
            if "Note" in data or "Information" in data:
                print(f"API WARNING for {symbol}: {data}")
                continue

            successful_data.append(data)
            print(f"SUCCESS: Fetched full data for {symbol}")
            time.sleep(20)

        except Exception as e:
            print(f"ERROR with {symbol}: {e}")

    if successful_data:
        fieldnames = list(successful_data[0].keys())
        try:
            with open(OUTPUT_FILE, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(successful_data)

            print(f"\nDone! Saved {len(successful_data)} instruments to file: {OUTPUT_FILE}")
            print(f"Found {len(fieldnames)} data columns.")
            
        except IOError as e:
             print(f"\nFile Error: Could not write to {OUTPUT_FILE}. Details: {e}")
    else:
        print("\nNo data fetched. Check your API key or symbol list.")

if __name__ == "__main__":
    main()