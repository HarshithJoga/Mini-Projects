from flask import Flask, render_template, request,redirect,url_for
import google.generativeai as genai
from dotenv import load_dotenv
import os
import sqlite3

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "users.db")
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
conn = get_db_connection()
conn.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')
conn.commit()
conn.close()

# Create Flask app
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    response_text = ""

    if request.method == "POST":
        prompt = request.form.get("prompt")
        if prompt:
            response = model.generate_content(prompt)
            response_text = response.text

    return render_template("index.html", response=response_text)

if __name__ == "__main__":
    app.run(debug=True)