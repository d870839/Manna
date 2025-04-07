import sqlite3
import os

db_path = '/opt/render/project/name/counter.db'
log_path = '/opt/render/project/name/init_db_log.txt'

with open(log_path, 'w') as log_file:
    log_file.write("Database initialization started\n")

try:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Create the 'stats' table to match Flask app
    c.execute('''
        CREATE TABLE IF NOT EXISTS stats (
            id INTEGER PRIMARY KEY,
            counter INTEGER,
            goal INTEGER,
            count1 INTEGER,
            count2 INTEGER,
            count3 INTEGER,
            count4 INTEGER,
            count5 INTEGER,
            count6 INTEGER,
            count7 INTEGER,
            count8 INTEGER
        )
    ''')

    # Insert initial row if table is empty
    c.execute('SELECT COUNT(*) FROM stats')
    if c.fetchone()[0] == 0:
        c.execute('''
            INSERT INTO stats
            (id, counter, goal, count1, count2, count3, count4, count5, count6, count7, count8)
            VALUES (1, 0, 100000, 0, 0, 0, 0, 0, 0, 0, 0)
        ''')

    conn.commit()
    conn.close()

    with open(log_path, 'a') as log_file:
        log_file.write("Database initialized successfully\n")

except Exception as e:
    with open(log_path, 'a') as log_file:
        log_file.write(f"Error during initialization: {e}\n")
