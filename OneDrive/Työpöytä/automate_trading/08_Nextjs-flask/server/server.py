from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

# Position table operations
from DataDealer import fetch_data, insert_data, update_current_stock_prices, delete_data_by_symbol, calculate_and_update_values, calculate_and_update_allocations, calculate_and_update_changes,update_average_price_and_quantity,decrease_quantity  # Assuming insert_data is a function to insert data into the database

# Activity table operations
from db_activitytable import fetch_activity_data, insert_activity_data


# app instance
app = Flask(__name__)
CORS(app)

update_current_stock_prices()
calculate_and_update_values()
calculate_and_update_allocations()
calculate_and_update_changes()

# GET route to fetch all risk levels
@app.route("/api/home", methods=['GET'])
def get_positions_data():
    try:
        

        df = fetch_data()
        data = df.to_dict(orient='records')


        return jsonify({'status': 'success', 'data': data})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500



# POST route to insert new data
@app.route("/api/positions", methods=['POST'])
def add_position():
    try:
        # Get the JSON data from the request
        data = request.get_json()
        print('Received Data:', data)  # Log incoming data for debugging
        selected_option = data.get('selectedOption')
        print(selected_option)

        if selected_option == 'Entry':
            insert_data(data)  # Assuming insert_data handles the actual database insertion
        elif selected_option == 'Exit':
            delete_data_by_symbol(data.get('symbol'), data.get('price'),data.get('quantity'))
        elif selected_option == 'Add':
            update_average_price_and_quantity(data.get('symbol'), data.get('price'),data.get('quantity'))
        elif selected_option == 'Trim':
            decrease_quantity(data.get("symbol"),data.get('price'),data.get('quantity'))
    
        return jsonify({'status': 'success', 'message': 'Data inserted successfully'})
    
    except ValueError as e:
        # Handle duplicate symbol error
        return jsonify({'status': 'error', 'message': str(e)}), 400
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'An unexpected error occurred'}), 500

if __name__ == "__main__":
    app.run(debug=True, port=8080)
