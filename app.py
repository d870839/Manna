from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect("counter.db") as conn:
        c = conn.cursor()
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
        c.execute('SELECT COUNT(*) FROM stats')
        if c.fetchone()[0] == 0:
            c.execute('INSERT INTO stats VALUES (1, 0, 100000, 0, 0, 0, 0, 0, 0, 0, 0)')
        conn.commit()

@app.route('/')
def index():
    return render_template('index.html')  # your current HTML goes in templates/index.html

@app.route('/update')
def update():
    amount = int(request.args.get('amount', 0))

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Get current total and goal
    cursor.execute("SELECT total, goal FROM counter")
    total, goal = cursor.fetchone()

    if total >= goal:
        conn.close()
        return jsonify({"counter": total, "counts": get_counts(), "goal_reached": True})

    # Update total
    new_total = total + amount
    cursor.execute("UPDATE counter SET total = ? WHERE rowid = 1", (new_total,))

    # Update the right count based on the amount
    index_map = {
        4000: 'count1',
        2400: 'count2',
        1200: 'count3',
        600:  'count4',
        5000: 'count5',
        1000: 'count6',
        500:  'count7',
        250:  'count8'
    }

    if amount in index_map:
        cursor.execute(f"UPDATE counter SET {index_map[amount]} = {index_map[amount]} + 1 WHERE rowid = 1")

    conn.commit()

    # Return updated data
    cursor.execute("SELECT total FROM counter")
    new_total = cursor.fetchone()[0]
    counts = get_counts(cursor)
    conn.close()

    return jsonify({"counter": new_total, "counts": counts, "goal_reached": new_total >= goal})


# Utility to return counts as a list
def get_counts(cursor=None):
    close_conn = False
    if cursor is None:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        close_conn = True

    cursor.execute("SELECT count1, count2, count3, count4, count5, count6, count7, count8 FROM counter")
    counts = list(cursor.fetchone())

    if close_conn:
        conn.close()

    return counts
@app.route('/reset')
def reset():
    password = request.args.get('password')
    if password != "Lori2025":
        return jsonify({"success": False})

    with sqlite3.connect("counter.db") as conn:
        c = conn.cursor()
        c.execute("""
            UPDATE stats SET counter = 0, count1 = 0, count2 = 0, count3 = 0,
            count4 = 0, count5 = 0, count6 = 0, count7 = 0, count8 = 0 WHERE id = 1
        """)
        conn.commit()
    return jsonify({"success": True})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=10000)
