from flask import Flask, request, jsonify, render_template
import io
from model_utils import predict_image
import traceback
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/predict", methods=["POST"])
def api_predict():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        img_bytes = io.BytesIO(request.files["file"].read())
        result = predict_image(img_bytes)
        return jsonify(result)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
