import sqlite3
import json

def create_country_table():
    conn = sqlite3.connect('nobel.sqlite3')
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Countries (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        code TEXT
                    )''')
    
    conn.commit()
    conn.close()

def load_country_data():
    conn = sqlite3.connect('nobel.sqlite3')
    cursor = conn.cursor()

    with open('country.json') as f:
        data = json.load(f)['countries']

        for country in data:
            cursor.execute('''INSERT INTO Countries (name, code)
                              VALUES (?, ?)''',
                            (country['name'], country.get('code', None)))

    conn.commit()
    conn.close()

create_country_table()
load_country_data()
