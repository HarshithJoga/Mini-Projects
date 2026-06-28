from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
from google import genai
import json
load_dotenv()
app = Flask(__name__)
# Gemini Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        topic = request.form['topic']
        difficulty = request.form['difficulty']
        prompt = f"""
        Create 5 {difficulty} difficulty multiple choice questions on {topic}.
        Questions must match the difficulty level.
        STRICT JSON FORMAT:
        [
        {{
              "question": "",
              "options": ["", "", "", ""],
              "answer": "",
              "explanation": ""
              }}
              ]"""


        # prompt = f"""
        # Create 10 multiple choice questions on {topic}.
        # Provide output strictly in JSON format.
        # Format:
        # [
        #   {{
        #     "question": "",
        #     "options": ["", "", "", ""],
        #     "answer": ""
        #   }}
        # ]
        # """
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )
        quiz_data = json.loads(response.text)
        return render_template("quiz.html", quiz=quiz_data)
    return render_template("index.html")

# @app.route('/submit', methods=['POST'])
# def submit():
#     score = 0
#     total = 0
#     for key in request.form:
#         # Only process question keys (q0, q1, q2...)
#         if key.startswith("q"):
#             user_answer = request.form.get(key)
#             correct_answer = request.form.get(f"ans_{key}")
#             total += 1
#             if user_answer == correct_answer:
#                 score += 1

#     return render_template("result.html", score=score, total=total)
@app.route('/submit', methods=['POST'])
def submit():
    results = []
    score = 0

    quiz = request.form.getlist("question")  # optional if stored earlier

    for key in request.form:
        if key.startswith("q"):
            user_answer = request.form.get(key)
            correct_answer = request.form.get(f"ans_{key}")
            explanation = request.form.get(f"exp_{key}")

            is_correct = user_answer == correct_answer
            if is_correct:
                score += 1

            results.append({
                "question": key,
                "user_answer": user_answer,
                "correct_answer": correct_answer,
                "is_correct": is_correct,
                "explanation": explanation
            })

    total = len(results)
    return render_template("result.html", score=score, total=total, results=results)

if __name__ == "__main__":
    app.run(debug=True)


















































































# from flask import Flask, render_template, request, jsonify
# import google.generativeai as genai
# from dotenv import load_dotenv
# import os

# from functions import save_note, get_note, generate_quiz
# from memory import add_to_memory, get_memory

# load_dotenv()
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# app = Flask(__name__)
# model = genai.GenerativeModel(
#     model_name="gemini-flash-latest",
#     system_instruction="""
# You are an AI Study Assistant.
# Explain topics clearly for students.
# If user asks to save notes, call save_note.
# If user asks for notes, call get_note.
# If user asks quiz, call generate_quiz.
# Respond in simple language.
# """
# )

# @app.route("/", methods=["GET", "POST"])
# def index():
#     response_text = ""

#     if request.method == "POST":
#         user_input = request.form["question"]

#         add_to_memory("user", user_input)

#         chat = model.start_chat(history=get_memory())
#         response = chat.send_message(user_input)

#         response_text = response.text
#         add_to_memory("assistant", response_text)

#     return render_template("hello.html", response=response_text)

# @app.route("/save", methods=["POST"])
# def save():
#     topic = request.form["topic"]
#     content = request.form["content"]
#     result = save_note(topic, content)
#     return jsonify(result)

# @app.route("/note", methods=["POST"])
# def note():
#     topic = request.form["topic"]
#     return jsonify(get_note(topic))

# @app.route("/quiz", methods=["POST"])
# def quiz():
#     topic = request.form["topic"]
#     return jsonify(generate_quiz(topic))




# if __name__ == "__main__":
#     app.run(debug=True)