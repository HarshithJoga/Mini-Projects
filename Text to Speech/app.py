import os
import uuid
from flask import Flask, request, send_file
import google.generativeai as genai
from gtts import gTTS
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("api")
if not API_KEY:
    raise RuntimeError("Gemini API key is missing")

genai.configure(api_key=API_KEY)

app = Flask(__name__)

# ==========================
# COMMON BACKGROUND STYLE
# ==========================
BACKGROUND_STYLE = """
    body {
        margin: 0;
        height: 100vh;
        background: linear-gradient(135deg, #667eea, #764ba2, #6b8cff);
        background-size: 300% 300%;
        animation: gradientMove 10s ease infinite;
        display: flex;
        justify-content: center;
        align-items: center;
        font-family: Inter, system-ui, sans-serif;
    }

    @keyframes gradientMove {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .card {
        background: rgba(255, 255, 255, 0.95);
        width: 600px;
        padding: 35px;
        border-radius: 18px;
        box-shadow: 0 30px 70px rgba(0,0,0,0.25);
    }
"""

# ==========================
# HOME PAGE
# ==========================
@app.route("/", methods=["GET"])
def text_form():
    return f"""
<!DOCTYPE html>
<html>
<head>
    <title>Text to Audio AI</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * {{ box-sizing: border-box; }}
        {BACKGROUND_STYLE}

        h1 {{
            text-align: center;
            color: #222;
            margin-bottom: 8px;
        }}

        p {{
            text-align: center;
            color: #555;
            margin-bottom: 25px;
        }}

        textarea {{
            width: 100%;
            min-height: 140px;
            padding: 14px;
            border-radius: 12px;
            border: 1px solid #ddd;
            font-size: 15px;
            outline: none;
        }}

        textarea:focus {{
            border-color: #667eea;
        }}

        button {{
            width: 100%;
            margin-top: 20px;
            padding: 14px;
            font-size: 16px;
            font-weight: 600;
            color: white;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border: none;
            border-radius: 12px;
            cursor: pointer;
            transition: 0.2s ease;
        }}

        button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 12px 30px rgba(102,126,234,0.45);
        }}

        footer {{
            margin-top: 18px;
            text-align: center;
            font-size: 12px;
            color: #888;
        }}
    </style>
</head>
<body>
    <div class="card">
        <h1>Text → Audio AI</h1>
        <p>Generate smart responses and listen instantly</p>

        <form action="/result" method="post">
            <textarea name="text" placeholder="Enter your prompt here..." required></textarea>
            <button type="submit">Generate Audio</button>
        </form>

        <footer>Powered by Gemini & Google TTS</footer>
    </div>
</body>
</html>
"""


# ==========================
# RESULT PAGE
# ==========================
@app.route("/result", methods=["POST"])
def result():
    user_text = request.form.get("text")

    model = genai.GenerativeModel("gemini-flash-latest")
    response = model.generate_content(user_text)
    generated_text = response.text

    filename = f"{uuid.uuid4().hex}.mp3"
    gTTS(generated_text, lang="en").save(filename)

    return f"""
<!DOCTYPE html>
<html>
<head>
    <title>Audio Result</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * {{ box-sizing: border-box; }}
        {BACKGROUND_STYLE}

        h2 {{
            color: #222;
            margin-bottom: 10px;
        }}

        .output {{
            background: #f4f6f8;
            padding: 18px;
            border-radius: 12px;
            font-size: 15px;
            line-height: 1.6;
            max-height: 220px;
            overflow-y: auto;
        }}

        audio {{
            width: 100%;
            margin-top: 15px;
        }}

        .actions {{
            margin-top: 25px;
            text-align: center;
        }}

        a {{
            text-decoration: none;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 12px 22px;
            border-radius: 12px;
            font-weight: 600;
            transition: 0.2s ease;
        }}

        a:hover {{
            transform: translateY(-2px);
            box-shadow: 0 12px 30px rgba(102,126,234,0.45);
        }}
    </style>
</head>
<body>
    <div class="card">
        <h2>Generated Text</h2>
        <div class="output">{generated_text}</div>

        <h2 style="margin-top: 25px;">Audio Output</h2>
        <audio controls>
            <source src="/audio/{filename}" type="audio/mpeg">
        </audio>

        <div class="actions">
            <a href="/">Generate Another</a>
        </div>
    </div>
</body>
</html>
"""


# ==========================
# SERVE AUDIO
# ==========================
@app.route("/audio/<filename>")
def serve_audio(filename):
    return send_file(filename, mimetype="audio/mpeg")


if __name__ == "__main__":
    app.run(debug=True)
