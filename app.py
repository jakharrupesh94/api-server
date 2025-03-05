from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Database setup
DATABASE = 'data.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

# Initialize the database
init_db()

@app.route('/data', methods=['POST'])
def add_data():
    data = request.json
    if not data or 'content' not in data:
        return jsonify({"error": "Missing 'content' in request"}), 400

    content = data['content']

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO entries (content) VALUES (?)', (content,))
        conn.commit()

    return jsonify({"message": "Data added successfully"}), 201

@app.route('/data', methods=['GET'])
def get_data():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM entries')
        rows = cursor.fetchall()

    data = [{"id": row[0], "content": row[1], "timestamp": row[2]} for row in rows]
    return jsonify(data), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)