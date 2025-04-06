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
    amount = int(request.args.get('amount'))
    with sqlite3.connect("counter.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM stats WHERE id = 1")
        row = c.fetchone()
        counter, goal = row[1], row[2]
        if counter >= goal:
            return jsonify({"counter": counter, "goal_reached": True})

        counter += amount
        counts = list(row[3:])
        amount_map = {4000: 0, 2400: 1, 1200: 2, 600: 3, 5000: 4, 1000: 5, 500: 6, 250: 7}
        index = amount_map[amount]
        counts[index] += 1

        c.execute("""
            UPDATE stats SET counter=?, count1=?, count2=?, count3=?, count4=?,
            count5=?, count6=?, count7=?, count8=? WHERE id = 1
        """, (counter, *counts))
        conn.commit()

        return jsonify({
            "counter": counter,
            "goal_reached": counter >= goal
        })
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
