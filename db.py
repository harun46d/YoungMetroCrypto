import sqlite3

conn = sqlite3.connect('crypto_prices.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS prices (
        symbol TEXT PRIMARY KEY,
        price REAL,
        price_change REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS price_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT,
        price REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()
conn.close()

def save_pairs_to_db(pairs):
    top_gainer = []
    with sqlite3.connect('crypto_prices.db') as conn:
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM price_history')

        for symbol, new_price, timestamp in pairs:
            cursor.execute('SELECT price FROM prices WHERE symbol = ?', (symbol,))
            row = cursor.fetchone()

            if row:
                old_price = row[0]
                price_change = ((new_price - old_price) / old_price) * 100
                
                cursor.execute('''
                    UPDATE prices
                    SET price = ?, price_change = ?, timestamp = ?
                    WHERE symbol = ?
                ''', (new_price, price_change, timestamp, symbol))
                
                if (price_change >= 7) or (price_change <= -7):
                    top_gainer.append({'symbol': symbol, 
                                        'price_change': price_change, 
                                        'current_price': new_price, 
                                        'previous_price': old_price})

                # Den alten Preis in der history-Tabelle speichern
                cursor.execute('''
                    INSERT INTO price_history (symbol, price, timestamp)
                    VALUES (?, ?, ?)
                ''', (symbol, old_price, timestamp))

            else:
                # Neues Handelspaar in der prices-Tabelle einfügen
                cursor.execute('''
                    INSERT INTO prices (symbol, price, timestamp)
                    VALUES (?, ?, ?)
                ''', (symbol, new_price, timestamp))

        if top_gainer:
            return top_gainer
        else:
            return None 
        
        conn.commit()