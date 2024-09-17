import yahoo_fin.stock_info as si

# Function to fetch latest stock prices for a list of tickers, skipping 'CASH'
def get_latest_stock_prices(tickers: list) -> dict:
    stock_data = {}

    for ticker in tickers:
        if ticker == 'CASH':
            continue  # Skip 'CASH' ticker entirely
        try:
            # Fetch the latest stock price
            stock_data[ticker] = si.get_live_price(ticker)
        except Exception as error:
            print(f"Error fetching stock data for {ticker}: {error}")
            stock_data[ticker] = None  # Set None if there's an error

    return stock_data

