import json
import os

# Load the ATM data from the JSON file
def load_atm_data(filename="atm_db.json"):
    if not os.path.exists(filename):
       return {
            "accounts": [
                {"account_number": "123456", "pin": "0000", "balance": 0.0, "statements": []}
            ]
        } 
    with open(filename, "r") as file:
        data = json.load(file)
    return data

# Save the ATM data to the JSON file
def save_atm_data(data, filename="atm_db.json"):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)
        
#Test the loading and saving functions



