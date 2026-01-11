import requests
import csv
import time

API_KEY = 'token'
OUTPUT_FILE = 'macro_2025_data.csv' 
TARGET_YEAR = '2025'

indicators_config = [
    {
        'column_name': 'treasury_yield_2y',
        'function': 'TREASURY_YIELD',
        'params': {'interval': 'monthly', 'maturity': '2year'}
    },
    {
        'column_name': 'treasury_yield_10y',
        'function': 'TREASURY_YIELD',
        'params': {'interval': 'monthly', 'maturity': '10year'}
    },
    {
        'column_name': 'federal_funds_rate',
        'function': 'FEDERAL_FUNDS_RATE',
        'params': {'interval': 'monthly'}
    },
    {
        'column_name': 'cpi',
        'function': 'CPI',
        'params': {'interval': 'monthly'}
    },
    {
        'column_name': 'unemployment_rate',
        'function': 'UNEMPLOYMENT',
        'params': {'interval': 'monthly'}
    }
]

def fetch_indicator_data(config):
    func = config['function']
    url = f'https://www.alphavantage.co/query?function={func}&apikey={API_KEY}'
    for key, value in config['params'].items():
        url += f"&{key}={value}"
        
    print(f"fetching: {config['column_name']} ({func})...")
    
    try:
        r = requests.get(url)
        data = r.json()
        
        if "Note" in data:
            print(f"  warning api limit: {data['Note']}")
            return None
        if "data" not in data:
            print(f"  -> error, lack of data.")
            return None
        result_dict = {item['date']: item['value'] for item in data['data']}
        return result_dict

    except Exception as e:
        print(f"  -> Wyjątek: {e}")
        return None

def main():
    merged_data = {}
    all_dates = set()

    print(f"start fetchinf data from {TARGET_YEAR}.")
    for config in indicators_config:
        col_name = config['column_name']
        indicator_data = fetch_indicator_data(config)
        
        if indicator_data:
            all_dates.update(indicator_data.keys())
            for date_str, value in indicator_data.items():
                if date_str not in merged_data:
                    merged_data[date_str] = {}
                merged_data[date_str][col_name] = value
        
        time.sleep(15)

    if merged_data:
        sorted_dates = sorted(list(all_dates), reverse=True)
        filtered_dates = [d for d in sorted_dates if d.startswith(TARGET_YEAR)]
        
        if not filtered_dates:
            print(f"data not found for year {TARGET_YEAR}!")
        else:
            fieldnames = ['date'] + [cfg['column_name'] for cfg in indicators_config]
            
            with open(OUTPUT_FILE, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for date_str in filtered_dates:
                    row = {'date': date_str}
                    data_for_date = merged_data.get(date_str, {})
                    
                    for cfg in indicators_config:
                        col = cfg['column_name']
                        row[col] = data_for_date.get(col, '')
                    
                    writer.writerow(row)

            print(f"\nDone! Saved data for {len(filtered_dates)} dates to file: {OUTPUT_FILE}")
    else:
        print("no data fetched!")

if __name__ == "__main__":
    main()