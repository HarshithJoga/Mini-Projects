from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai
import os
load_dotenv()
app = Flask(__name__)
# Gemini setup
genai.configure(api_key=os.getenv("api"))
model = genai.GenerativeModel("gemini-2.5-flash")
@app.route("/")
def index():
    return render_template("image.html")
@app.route("/generate", methods=["POST"])
def generate_caption():
    try:
        data = request.get_json(force=True)
        platform = data["platform"]
        topic = data["topic"]
        tone = data["tone"]
        prompt = f"""
        Generate 5 {tone} captions for {platform} about "{topic}".
        Also generate relevant hashtags.
        """
        response = model.generate_content(prompt)
        print(response)
        return jsonify({
            "result": response.text
        })
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True)