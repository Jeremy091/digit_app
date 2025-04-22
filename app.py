# app.py
from flask import Flask, render_template, request, jsonify
from model_utils import predict_image
import io

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/predict", methods=["POST"])
def api_predict():
    if "file" not in request.files:
        return jsonify({"error": "No hay imagen"}), 400
    file = request.files["file"]
    img_bytes = io.BytesIO(file.read())
    result = predict_image(img_bytes)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
