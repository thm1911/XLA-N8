from flask import Flask, request, jsonify, render_template
from processor import extract_characters_from_image_handwriting
from prediction import get_predicted_text
import os
import tensorflow as tf

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["image"]

    save_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(save_path)

    chars = extract_characters_from_image_handwriting(save_path)

    result_text = get_predicted_text(chars)
    print(result_text)

    return jsonify({
        "image_url": "/" + save_path,
        "prediction": result_text
    })

if __name__ == "__main__":
    app.run(debug=True)
