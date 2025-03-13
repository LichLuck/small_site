from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/init_db', methods=['GET'])
def init_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS items (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        location TEXT NOT NULL)''')
    conn.commit()
    conn.close()
    return 'Database initialized!', 200

@app.route('/skl/')
def hello():
    return "Привет из /skl/"

@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    name = data.get('name')
    location = data.get('location')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO items (name, location) VALUES (?, ?)', (name, location))
    conn.commit()
    item_id = cursor.lastrowid
    conn.close()
    return jsonify({'id': item_id, 'name': name, 'location': location}), 201

@app.route('/items', methods=['GET'])
def get_items():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM items').fetchall()
    conn.close()
    return jsonify([dict(item) for item in items])

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM items WHERE id = ?', (item_id,)).fetchone()
    conn.close()
    if item is None:
        return jsonify({'error': 'Item not found'}), 404
    return jsonify(dict(item))

@app.route('/', methods=['GET'])
def get_items_html():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM items').fetchall()
    conn.close()
    return render_template('items.html', items=items)

if __name__ == '__main__':
    app.run(debug=False, port=5001)