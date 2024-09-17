import psycopg2
import pandas as pd
from config import config
from datetime import datetime
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


# Function to connect to the database
def connect_db():
    """Connect to the PostgreSQL database and return the connection object."""
    connection = None
    try:
        # Get connection parameters from the config
        params = config()
        print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(**params)
        return connection
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        return None

# Function to fetch data from the Positions table
def fetch_data():
    """Fetch data from the Positions table."""
    connection = connect_db()

    try:
        # Create a cursor
        crsr = connection.cursor()

        # SQL query to fetch all data from Positions table
        select_query = "SELECT * FROM Positions;"
        crsr.execute(select_query)

        # Fetch all rows and get column names
        rows = crsr.fetchall()
        columns = [desc[0] for desc in crsr.description]

        # Convert to DataFrame
        df = pd.DataFrame(rows, columns=columns)
       
        return df

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error fetching data: {error}")
    finally:
        if connection is not None:
            connection.close()
            print('Database connection terminated.')


def insert_data(row):
    """Insert a single row into the Positions table if the symbol does not already exist."""
    connection = connect_db()

    try:
        # Create a cursor
        crsr = connection.cursor()

        # Check if the symbol already exists
        check_query = "SELECT 1 FROM Positions WHERE symbol = %s;"
        crsr.execute(check_query, (row['symbol'],))
        exists = crsr.fetchone()

        if exists:
            raise ValueError(f"Symbol {row['symbol']} already exists in the database.")

        # Get today's date in 'YYYY-MM-DD' format
        today_date = datetime.today().strftime('%Y-%m-%d')

        # Set default values for fields not provided in the row
        allocation = row.get('allocation', 0)
        avg_cost = row.get('avg_cost', 0)
        value = row.get('value', 0)
        current_price = row.get('price', 0)  # Use 'price' from the row data
        change = row.get('change', 0)

        # SQL query to insert a single row into the Positions table
        insert_query = """
            INSERT INTO Positions (allocation, symbol, quantity, open_date, avg_cost, value, current_price, change)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        # Execute the insert query with the row data
        crsr.execute(insert_query, (
            allocation, 
            row['symbol'], 
            row['quantity'], 
            today_date,  # Use today's date as open_date
            row['price'], 
            value, 
            current_price,  # Use the 'price' field from the row
            change
        ))

        # Commit the transaction
        connection.commit()
        print('Row inserted successfully in Positions table.')

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error inserting data: {error}")
        raise
    finally:
        if connection is not None:
            connection.close()
            print('Database connection terminated.')


# Function to update stock prices in the Positions table
def update_current_stock_prices():

    """Fetch latest stock prices and update the Positions table."""
    # Fetch data from the database
    df = fetch_data()

    # Extract distinct symbols from the DataFrame
    symbols = df['symbol'].unique().tolist()

    # Get latest stock prices for the symbols
    stock_prices = get_latest_stock_prices(symbols)
    
    connection = connect_db()

    try:
        # Create a cursor
        crsr = connection.cursor()

        # Update prices in the Positions table
        for symbol, price in stock_prices.items():
            if price is None:
                continue  # Skip if the price could not be fetched
            update_query = """
                UPDATE Positions
                SET current_price = %s
                WHERE symbol = %s;
            """
            crsr.execute(update_query, (price, symbol))

        # Commit the transaction
        connection.commit()
        print('Stock prices updated successfully in Positions table.')

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error updating stock prices: {error}")
    finally:
        if connection is not None:
            connection.close()
            print('Database connection terminated.')


# Jos exit niin tätä kutsutaan
# Function to delete a row from the Positions table by symbol
def delete_data_by_symbol(symbol: str):

    """Delete a row from the Positions table based on the symbol."""
    connection = connect_db()

    try:
        # Create a cursor
        crsr = connection.cursor()

        # Check if the symbol exists
        check_query = "SELECT 1 FROM Positions WHERE symbol = %s;"
        crsr.execute(check_query, (symbol,))
        exists = crsr.fetchone()

        if not exists:
            raise ValueError(f"Symbol {symbol} does not exist in the database.")

        # SQL query to delete a row based on the symbol
        delete_query = """
            DELETE FROM Positions
            WHERE symbol = %s;
        """
        # Execute the delete query with the symbol
        crsr.execute(delete_query, (symbol,))

        # Commit the transaction
        connection.commit()
        print(f'Row with symbol {symbol} deleted successfully from Positions table.')

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error deleting data: {error}")
        raise
    finally:
        if connection is not None:
            connection.close()
            print('Database connection terminated.')



# Käy laskemassa kunkin position arvon nykyisellä hinnalla ja asettaa value kentän
def calculate_and_update_values():

    df = fetch_data()
    connection = connect_db()

    try:
        # Create a cursor
        crsr = connection.cursor()

        # Loop through each row in the DataFrame and calculate value
        for index, row in df.iterrows():
            symbol = row['symbol']
            quantity = row['quantity']
            current_price = row['current_price']

            if symbol == 'CASH':
                # If symbol is CASH, set value to quantity
                value = quantity
            else:
                # Calculate value as quantity * current_price
                if current_price is not None and quantity is not None:
                    value = quantity * current_price
                else:
                    value = 0  # Set value to 0 if current_price or quantity is None

            # Update the value in the Positions table
            update_query = """
                UPDATE Positions
                SET value = %s
                WHERE symbol = %s;
            """
            crsr.execute(update_query, (round(value, 2), symbol))

        # Commit the transaction
        connection.commit()
        print('Values updated successfully in Positions table.')

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error updating values: {error}")
    finally:
        if connection is not None:
            connection.close()
            print('Database connection terminated.')



def calculate_and_update_allocations():
    """Calculate the allocation for each position and update the Positions table."""
    # Fetch data from the database
    df = fetch_data()

    connection = connect_db()

    try:
        # Create a cursor
        crsr = connection.cursor()

        # Calculate the total sum of the value column
        total_value = df['value'].sum()
        
        if total_value == 0:
            print("Total value is zero. Allocation calculation will be skipped.")
            return

        # Loop through each row in the DataFrame and calculate allocation
        for index, row in df.iterrows():
            symbol = row['symbol']
            value = row['value']

            if value is not None and total_value > 0:
                # Calculate the allocation
                allocation = (value / total_value)*100

                # Update the allocation in the Positions table
                update_query = """
                    UPDATE Positions
                    SET allocation = %s
                    WHERE symbol = %s;
                """
                crsr.execute(update_query, (round(allocation, 2), symbol))

        # Commit the transaction
        connection.commit()
        print('Allocations updated successfully in Positions table.')

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error updating allocations: {error}")
    finally:
        if connection is not None:
            connection.close()
            print('Database connection terminated.')



def calculate_and_update_changes():
    """Calculate the change for each position and update the Positions table."""
    # Fetch data from the database
    df = fetch_data()

    connection = connect_db()

    try:
        # Create a cursor
        crsr = connection.cursor()

        # Loop through each row in the DataFrame and calculate change
        for index, row in df.iterrows():
            symbol = row['symbol']
            current_price = row['current_price']
            avg_cost = row['avg_cost']

            if current_price is not None and avg_cost is not None and current_price != 0:
                # Calculate the change
                change = ((current_price - avg_cost) / current_price*100)

                # Update the change in the Positions table
                update_query = """
                    UPDATE Positions
                    SET change = %s
                    WHERE symbol = %s;
                """
                crsr.execute(update_query, (round(change, 2), symbol))

        # Commit the transaction
        connection.commit()
        print('Changes updated successfully in Positions table.')

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error updating changes: {error}")
    finally:
        if connection is not None:
            connection.close()
            print('Database connection terminated.')


# Addaa positioon
def update_average_price_and_quantity(symbol: str, new_price: float, new_quantity: int):
    """Calculate and update the new average price and quantity for a given position in the database."""
    # Fetch data from the database
    df = fetch_data() 
    connection = connect_db()

    try:
        # Create a cursor
        crsr = connection.cursor()

        # Check if the symbol exists in the database
        if symbol not in df['symbol'].values:
           raise ValueError(f"Symbol '{symbol}' not found in the database.")

        # Fetch the current average price and quantity for the given symbol
        current_data = df[df['symbol'] == symbol].iloc[0]
        current_avg_price = current_data['avg_cost']
        current_quantity = current_data['quantity']

        # Convert numpy types to regular Python types
        current_avg_price = float(current_avg_price)
        current_quantity = int(current_quantity)

        # Calculate the new average price
        total_value = (current_avg_price * current_quantity) + (new_price * new_quantity)
        total_quantity = current_quantity + new_quantity
        new_avg_price = total_value / total_quantity if total_quantity != 0 else 0

        # Update the average price and quantity in the Positions table
        update_query = """
            UPDATE Positions
            SET avg_cost = %s,
                quantity = %s
            WHERE symbol = %s;
        """
        crsr.execute(update_query, (round(new_avg_price, 2), total_quantity, symbol))

        # Commit the transaction
        connection.commit()
        print(f'Average price for {symbol} updated to {new_avg_price:.2f}. Quantity updated to {total_quantity}.')

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error updating average price and quantity: {error}")
        raise
    finally:
        if connection is not None:
            connection.close()
            print('Database connection terminated.')



# Trimmaa positiota
def decrease_quantity(symbol: str, quantity_to_decrease: int):
    """Decrease the quantity for a given symbol in the database."""
    # Fetch data from the database
    df = fetch_data()
    connection = connect_db()

    try:
        # Create a cursor
        crsr = connection.cursor()

        # Check if the symbol exists in the database
        if symbol not in df['symbol'].values:
            raise ValueError(f"Symbol '{symbol}' not found in the database.")

        # Fetch the current quantity for the given symbol
        current_data = df[df['symbol'] == symbol].iloc[0]
        current_quantity = current_data['quantity']

        # Convert numpy types to regular Python types
        current_quantity = int(current_quantity)

        # Ensure that the quantity to decrease does not exceed the current quantity
        if quantity_to_decrease > current_quantity:
            print(f"Quantity to decrease ({quantity_to_decrease}) exceeds current quantity ({current_quantity}) for symbol '{symbol}'.")
            return

        # Calculate the new quantity
        new_quantity = current_quantity - quantity_to_decrease

        # Update the quantity in the Positions table
        update_query = """
            UPDATE Positions
            SET quantity = %s
            WHERE symbol = %s;
        """
        crsr.execute(update_query, (new_quantity, symbol))

        # Commit the transaction
        connection.commit()
        print(f'Quantity for {symbol} decreased by {quantity_to_decrease}. New quantity is {new_quantity}.')

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error decreasing quantity: {error}")
        raise
    finally:
        if connection is not None:
            connection.close()
            print('Database connection terminated.')
