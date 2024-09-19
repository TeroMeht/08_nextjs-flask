import yahoo_fin.stock_info as si
import numpy as np

# Function to fetch latest stock prices for a list of tickers, skipping 'CASH'
def get_latest_stock_prices(tickers: list) -> dict:
    stock_data = {}

    for ticker in tickers:
        if ticker == 'CASH':
            continue  # Skip 'CASH' ticker entirely
        try:
            # Fetch the latest stock price
            price = si.get_live_price(ticker)
            
            # Convert np.float64 to native Python float if necessary
            if isinstance(price, np.float64):
                price = float(price)
            
            # Round to 2 decimal places
            rounded_price = round(price, 2)

            stock_data[ticker] = rounded_price
        except Exception as error:
            print(f"Error fetching stock data for {ticker}: {error}")
            stock_data[ticker] = None  # Set None if there's an error

    return stock_data

