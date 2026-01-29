

from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import datetime
from google import genai  # Gemini API SDK

app = Flask(__name__)

# Initialize Gemini Client
client = genai.Client(api_key="keyyyyyyy requireement")  # ← Insert your API key

# Initialize database
def init_db():
    conn = sqlite3.connect('moods.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS moods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mood INTEGER NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit-mood', methods=['POST'])
def submit_mood():
    data = request.get_json()
    mood = data.get('mood')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect('moods.db')
    c = conn.cursor()
    c.execute('INSERT INTO moods (mood, timestamp) VALUES (?, ?)', (mood, timestamp))
    conn.commit()
    conn.close()        

    return jsonify({'message': 'Your mood has been recorded. Thank you!'})

@app.route('/chatbot', methods=['POST'])
def chatbot():
    try:
        user_message = request.json.get('message')

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_message
        )

        bot_reply = response.text
        return jsonify({'botReply': bot_reply})
    
    except Exception as e:
        print(f"Error during chatbot API call: {e}")
        return jsonify({'botReply': 'Sorry, something went wrong.'}), 500


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
