import sqlite3
import os

db_path = 'database.db'
log_path = 'init_db_log.txt'

# Open log file
with open(log_path, 'w') as log_file:
    log_file.write("Database initialization started\n")

try:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Create counter table
    c.execute('''
    CREATE TABLE IF NOT EXISTS counter (
        id INTEGER PRIMARY KEY,
        value INTEGER DEFAULT 0,
        goal INTEGER DEFAULT 100000
    )
    ''')

    # Check if the table was created/initialized
    c.execute('SELECT COUNT(*) FROM counter')
    count = c.fetchone()[0]
    if count == 0:
        c.execute('INSERT INTO counter (value, goal) VALUES (0, 100000)')

    # Create button counts table
    c.execute('''
    CREATE TABLE IF NOT EXISTS button_counts (
        id INTEGER PRIMARY KEY,
        count INTEGER DEFAULT 0
    )
    ''')

    # Initialize button counts if they don't exist
    for i in range(1, 9):
        c.execute('INSERT OR IGNORE INTO button_counts (id, count) VALUES (?, 0)', (i,))

    conn.commit()
    conn.close()

    with open(log_path, 'a') as log_file:
        log_file.write("Database initialized successfully\n")
except Exception as e:
    with open(log_path, 'a') as log_file:
        log_file.write(f"Error during initialization: {e}\n")
