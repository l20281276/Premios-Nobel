import sqlite3
import json

def create_tables():
    conn = sqlite3.connect('nobel.sqlite3')
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Laureates (
                        laureate_id INTEGER PRIMARY KEY,
                        firstname TEXT,
                        surname TEXT,
                        born DATE,
                        died DATE,
                        bornCountry TEXT,
                        bornCountryCode TEXT,
                        bornCity TEXT,
                        diedCountry TEXT,
                        diedCountryCode TEXT,
                        diedCity TEXT,
                        gender TEXT
                    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS Prizes (
                        prize_id INTEGER PRIMARY KEY,
                        year INTEGER,
                        category TEXT
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Affiliations (
                        affiliation_id INTEGER PRIMARY KEY,
                        laureate_id INTEGER,
                        name TEXT,
                        city TEXT,
                        country TEXT,
                        FOREIGN KEY(laureate_id) REFERENCES Laureates(laureate_id)
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Laureate_Prizes (
                        laureate_id INTEGER,
                        prize_id INTEGER,
                        share INTEGER,
                        motivation TEXT,
                        FOREIGN KEY(laureate_id) REFERENCES Laureates(laureate_id),
                        FOREIGN KEY(prize_id) REFERENCES Prizes(prize_id),
                        PRIMARY KEY (laureate_id, prize_id)
                    )''')
    
    conn.commit()
    conn.close()

def load_laureate_data():
    conn = sqlite3.connect('nobel.sqlite3')
    cursor = conn.cursor()

    with open('laureate.json') as f:
        data = json.load(f)['laureates']

        for laureate in data:
            cursor.execute('''INSERT INTO Laureates (laureate_id, firstname, surname, born, died,
                            bornCountry, bornCountryCode, bornCity, diedCountry, diedCountryCode, diedCity, gender)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                            (laureate['id'], laureate.get('firstname', ''), laureate.get('surname', ''), 
                            laureate.get('born', None), laureate.get('died', None), 
                            laureate.get('bornCountry', ''), laureate.get('bornCountryCode', ''), 
                            laureate.get('bornCity', ''), laureate.get('diedCountry', ''), 
                            laureate.get('diedCountryCode', ''), laureate.get('diedCity', ''), 
                            laureate.get('gender', '')))

            laureate_id = laureate['id']
            
            for prize in laureate.get('prizes', []):
                prize_id = str(prize['year']) + "_" + prize['category']
                
                cursor.execute('''INSERT INTO Prizes (year, category)
                                  VALUES (?, ?)''',
                                (prize['year'], prize['category']))

                cursor.execute('''INSERT INTO Laureate_Prizes (laureate_id, prize_id, share, motivation)
                                  VALUES (?, ?, ?, ?)''',
                                (laureate_id, prize_id, prize['share'], prize['motivation']))

                for affiliation in prize.get('affiliations', []):
                    if isinstance(affiliation, dict):
                        cursor.execute('''INSERT INTO Affiliations (laureate_id, name, city, country)
                                          VALUES (?, ?, ?, ?)''',
                                        (laureate_id, affiliation.get('name', ''), 
                                        affiliation.get('city', ''), affiliation.get('country', '')))
                    else:
                        cursor.execute('''INSERT INTO Affiliations (laureate_id, name, city, country)
                                          VALUES (?, ?, ?, ?)''',
                                        (laureate_id, '', '', ''))

    conn.commit()
    conn.close()

create_tables()
load_laureate_data()
