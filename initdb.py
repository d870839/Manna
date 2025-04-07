import sqlite3

conn = sqlite3.connect('database.db')  # or the path you're using on Render
c = conn.cursor()

# Table to track the total counter and goal
c.execute('''
CREATE TABLE IF NOT EXISTS counter (
    id INTEGER PRIMARY KEY,
    value INTEGER DEFAULT 0,
    goal INTEGER DEFAULT 100000
)
''')

# Insert initial row if empty
c.execute('SELECT COUNT(*) FROM counter')
if c.fetchone()[0] == 0:
    c.execute('INSERT INTO counter (value, goal) VALUES (0, 100000)')

# Table to track how many times each button has been clicked
c.execute('''
CREATE TABLE IF NOT EXISTS button_counts (
    id INTEGER PRIMARY KEY,
    count INTEGER DEFAULT 0
)
''')

# Initialize counts for 8 buttons
for i in range(1, 9):
    c.execute('INSERT OR IGNORE INTO button_counts (id, count) VALUES (?, 0)', (i,))

conn.commit()
conn.close()
