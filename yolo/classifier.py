from flask import Blueprint, request, jsonify
from ultralytics import YOLO
import io
from PIL import Image

classifier_service = Blueprint("classifier", __name__)

model = YOLO("yolo11n-cls.pt")

@classifier_service.route("/classify", methods=["POST"])
def classify():
    file = request.files["image"]
    img_bytes = file.read()
    img = Image.open(io.BytesIO(img_bytes))

    results = model(img)
    
    formatted_results = []
    for r in results:
        try:
            top_probs_indices = r.probs.top5
            top_classes = [
                {
                    "name": r.names[top_probs_indices[i]],
                    "probability": float(r.probs.top5conf[i])
                }
                for i in range(len(top_probs_indices))
            ]
            formatted_results.append({"top_classes": top_classes})
        except AttributeError:
            return jsonify({"error": "Error processing results"}), 500

    return jsonify(formatted_results), 200
