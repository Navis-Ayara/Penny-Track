import json
import os
from datetime import datetime

def get_database():
    db_path = "database.json"
    if not os.path.exists(db_path):
        with open(db_path, "w") as file:
            json.dump([], file)
            return []
    with open(db_path, "r") as file:
        return json.load(file)

database = get_database()

def save_database(data):   
    db_path = "database.json"
    with open(db_path, "w") as file:
        json.dump(data, file, indent=4)

def add_entry(category, amount, date=datetime.now().strftime("%Y-%m-%d")):
    entry = {
        "category": category,
        "amount": amount,
        "date": date
    }
    database.append(entry)
    save_database(database)

def get_entries():
    return database

