from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('stories.db')
    conn.row_factory = sqlite3.Row
    return conn

def serialize_row(row):
    return {key: row[key] for key in row.keys()}

@app.route('/')
def index():
    conn = get_db_connection()
    stories = conn.execute('SELECT * FROM stories').fetchall()
    conn.close()
    serialized_stories = [serialize_row(story) for story in stories]
    return render_template('worldstory.html', stories=serialized_stories)

@app.route('/add_story', methods=['POST'])
def add_story():
    title = request.form['title']
    location = request.form['location']
    story = request.form['story']

    conn = get_db_connection()
    conn.execute('INSERT INTO stories (title, location, story) VALUES (?, ?, ?)',
                 (title, location, story))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)