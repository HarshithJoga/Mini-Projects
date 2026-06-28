from flask import Flask, render_template, request
from PIL import Image
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-flash-latest")
@app.route("/", methods=["GET", "POST"])
def index():
    image_data = None
    ai_description = None

    if request.method == "POST":
        file = request.files.get("image")

        if file:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            # Open image safely
            with Image.open(filepath) as img:
                image_data = {
                    "filename": file.filename,
                    "width": img.width,
                    "height": img.height,
                    "format": img.format,
                    "path": filepath
                }

            # Gemini Vision Analysis
            with Image.open(filepath) as img:
                response = model.generate_content(
                    [
                        "Describe this image clearly and simply.",
                        img
                    ]
                )
                ai_description = response.text

    return render_template(
        "main.html",
        image_data=image_data,
        ai_description=ai_description
    )

if __name__ == "__main__":
    app.run(debug=True)