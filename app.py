from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

DB_NAME = "counter.db"
TABLE_NAME = "stats"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute(f'''
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
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
        c.execute(f'SELECT COUNT(*) FROM {TABLE_NAME}')
        if c.fetchone()[0] == 0:
            c.execute(f'''
                INSERT INTO {TABLE_NAME} VALUES (1, 0, 100000, 0, 0, 0, 0, 0, 0, 0, 0)
            ''')
        conn.commit()
@app.route('/data')
def data():
    with sqlite3.connect({TABLE_NAME}) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT counter, goal, count1, count2, count3, count4, count5, count6, count7, count8 FROM {TABLE_NAME} WHERE id = 1")
        row = cursor.fetchone()
        return jsonify({
            "counter": row[0],
            "goal": row[1],
            "counts": list(row[2:])
        })
@app.route('/')
def index():
    return render_template('index.html')  # Make sure templates/index.html exists

@app.route('/update')
def update():
    amount = int(request.args.get('amount', 0))

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Get current counter and goal
    cursor.execute(f"SELECT counter, goal FROM {TABLE_NAME} WHERE id = 1")
    total, goal = cursor.fetchone()

    if total >= goal:
        conn.close()
        return jsonify({"counter": total, "counts": get_counts(), "goal_reached": True})

    # Update counter
    new_total = total + amount
    cursor.execute(f"UPDATE {TABLE_NAME} SET counter = ? WHERE id = 1", (new_total,))

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
        cursor.execute(f"UPDATE {TABLE_NAME} SET {index_map[amount]} = {index_map[amount]} + 1 WHERE id = 1")

    conn.commit()

    # Return updated data
    cursor.execute(f"SELECT counter FROM {TABLE_NAME} WHERE id = 1")
    new_total = cursor.fetchone()[0]
    counts = get_counts(cursor)
    conn.close()

    return jsonify({"counter": new_total, "counts": counts, "goal_reached": new_total >= goal})

# Utility to return counts as a list
def get_counts(cursor=None):
    close_conn = False
    if cursor is None:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        close_conn = True

    cursor.execute(f"""
        SELECT count1, count2, count3, count4, count5, count6, count7, count8
        FROM {TABLE_NAME} WHERE id = 1
    """)
    counts = list(cursor.fetchone())

    if close_conn:
        conn.close()

    return counts

@app.route('/reset', methods=['POST'])
def reset():
    password = request.form.get('password')

    # Check if the password is correct
    if password != "Lori2025":
        return jsonify({"success": False, "message": "Invalid password."})

    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute(f"""
            UPDATE {TABLE_NAME}
            SET counter = 0, count1 = 0, count2 = 0, count3 = 0,
                count4 = 0, count5 = 0, count6 = 0, count7 = 0, count8 = 0
            WHERE id = 1
        """)
        conn.commit()

    return jsonify({"success": True})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=10000)
