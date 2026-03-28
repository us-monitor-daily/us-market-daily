import json
import urllib.request
import urllib.error

def get_large_cap_movers():
    # TradingView scanner API endpoint
    url = 'https://scanner.tradingview.com/america/scan'
    
    # Required headers for the request
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    }
    
    # Payload targeting the US market large-cap companies
    # It sorts by market capitalization in descending order and fetches the top 20
    data = {
        "filter": [
            {"left": "market_cap_basic", "operation": "nempty"}
        ],
        "options": {"lang": "en"},
        "markets": ["america"],
        "symbols": {"query": {"types": []}, "tickers": []},
        "columns": [
            "name",              # Stock Symbol Name (e.g. AAPL)
            "description",       # Full Company Name
            "close",             # Current/Close Price
            "change",            # Percentage Change (등락률)
            "market_cap_basic"   # Market Capitalization
        ],
        "sort": {"sortBy": "market_cap_basic", "sortOrder": "desc"},
        "range": [0, 20]
    }
    
    req = urllib.request.Request(
        url, 
        data=json.dumps(data).encode('utf-8'), 
        headers=headers, 
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            extracted_data = []
            
            # Parse the JSON response and map the columns to standard fields
            for item in result.get('data', []):
                columns = item.get('d', [])
                if len(columns) >= 5:
                    ticker = columns[0]
                    name = columns[1]
                    price = columns[2]
                    change_percent = columns[3]
                    market_cap = columns[4]
                    
                    extracted_data.append({
                        "ticker": ticker,
                        "name": name,
                        "price_usd": price,
                        "change_percent": round(change_percent, 2),
                        "market_cap_usd": market_cap
                    })
            
            # Print the extracted data as formatted JSON
            print(json.dumps(extracted_data, indent=4, ensure_ascii=False))
            
    except urllib.error.URLError as e:
        print(f"Error fetching data from TradingView: {e}")

if __name__ == '__main__':
    get_large_cap_movers()
