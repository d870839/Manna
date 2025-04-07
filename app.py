@app.route('/data')
def get_data():
    conn = sqlite3.connect('counter.db')
    cursor = conn.cursor()

    # Get current counter value and goal
    cursor.execute("SELECT total, goal FROM counter WHERE id = 1")
    total, goal = cursor.fetchone()

    # Get current counts from the button_counts table
    counts = get_counts(cursor)

    conn.close()

    # Return the data as JSON
    return jsonify({
        "counter": total,
        "goal": goal,
        "counts": counts
    })

def update():
    amount = int(request.args.get('amount', 0))

    conn = sqlite3.connect('counter.db')  # Consistent database file
    cursor = conn.cursor()

    # Get current total and goal
    cursor.execute("SELECT total, goal FROM counter WHERE id = 1")
    total, goal = cursor.fetchone()

    if total >= goal:
        conn.close()
        return jsonify({"counter": total, "counts": get_counts(), "goal_reached": True})

    # Update total
    new_total = total + amount
    cursor.execute("UPDATE counter SET total = ? WHERE id = 1", (new_total,))

    # Update the right count based on the amount
    index_map = {
        4000: 1,
        2400: 2,
        1200: 3,
        600:  4,
        5000: 5,
        1000: 6,
        500:  7,
        250:  8
    }

    if amount in index_map:
        button_id = index_map[amount]
        cursor.execute(f"UPDATE button_counts SET count = count + 1 WHERE id = ?", (button_id,))

    conn.commit()

    # Return updated data
    cursor.execute("SELECT total FROM counter WHERE id = 1")
    new_total = cursor.fetchone()[0]
    counts = get_counts(cursor)
    conn.close()

    return jsonify({"counter": new_total, "counts": counts, "goal_reached": new_total >= goal})

# Utility to return counts from the 'button_counts' table
def get_counts(cursor=None):
    close_conn = False
    if cursor is None:
        conn = sqlite3.connect('counter.db')
        cursor = conn.cursor()
        close_conn = True

    cursor.execute("SELECT count FROM button_counts ORDER BY id")
    counts = [x[0] for x in cursor.fetchall()]

    if close_conn:
        conn.close()

    return counts
