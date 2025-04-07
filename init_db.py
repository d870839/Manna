import sqlite3
import os

db_path = '/opt/render/project/name/counter.db'  # Use persistent path
log_path = '/opt/render/project/name/init_db_log.txt'  # Log path for debugging

# Create/open the log file
with open(log_path, 'w') as log_file:
    log_file.write("Database initialization started\n")

try:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Create the 'counter' table if it doesn't exist
    c.execute('''
    CREATE TABLE IF NOT EXISTS counter (
        id INTEGER PRIMARY KEY,
        total INTEGER DEFAULT 0,
        goal INTEGER DEFAULT 100000
    )
    ''')

    # Check if the table was created/initialized
    c.execute('SELECT COUNT
