from db_connection import connect_db
import pandas as pd
from datetime import datetime
import psycopg2

# Tähän tauluun dataa menee vain yhteen suuntaan. Eli kun käyttäjä kirjaa formilta uuden aktiviteetin se kirjoitetaan tänne
# Täältä tarvii kuitenkin hakee kaikki data (ainakin aluksi) ja esittää se päänäytöllä. 

# Function to fetch data from the Activity table
def fetch_activity_data():
    """Fetch data from the Activity table."""
    connection = connect_db()

    try:
        # Create a cursor
        crsr = connection.cursor()

        # SQL query to fetch all data from Activity table
        select_query = "SELECT * FROM Activity;"
        crsr.execute(select_query)

        # Fetch all rows and get column names
        rows = crsr.fetchall()
        columns = [desc[0] for desc in crsr.description]

        # Convert to DataFrame
        df = pd.DataFrame(rows, columns=columns)
        
        return df

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error fetching data: {error}")
        raise
    finally:
        if connection is not None:
            connection.close()
            print('Database connection terminated.')


def insert_activity_data(row):
    connection = connect_db()

    try:
        # Create a cursor
        crsr = connection.cursor()

        # Get the next activityid
        crsr.execute("SELECT COALESCE(MAX(activityid), 0) + 1 FROM activity;")
        next_activityid = crsr.fetchone()[0]

        # Get today's date and time including minutes
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Calculate the value by multiplying price and quantity
        value = row['price'] * row['quantity']

        # SQL query to insert a single row into the Activity table
        insert_query = """
            INSERT INTO activity (activityid, operation, timestamp, quantity, price, value, symbol)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """

        # Data to be inserted
        data = (
            next_activityid,
            row['operation'],
            timestamp,
            row['quantity'],
            row['price'],
            value,  # Calculated value
            row['symbol']
        )

        # Execute the insert query
        crsr.execute(insert_query, data)

        # Commit the transaction
        connection.commit()

        print('Row inserted successfully into Activity table.')

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error inserting data: {error}")
        raise
    finally:
        if connection is not None:
            connection.close()
            print('Database connection terminated.')