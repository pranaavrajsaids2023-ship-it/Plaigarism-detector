from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# This handles the AI text verification processing
@app.route("/api/detect", methods=["POST"])
def detect_text():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "No text content provided"}), 400
    
    url = "https://api-inference.huggingface.co/models/roberta-base-openai-detector"
    
    try:
        response = requests.post(url, json={"inputs": data["text"]})
        result = response.json()
        
        if isinstance(result, list) and len(result) > 0:
            top_prediction = max(result[0], key=lambda x: x['score'])
            label = top_prediction['label']
            confidence = top_prediction['score'] * 100
            
            return jsonify({
                "verdict": "Human" if label == "Real" else "AI",
                "confidence": round(confidence, 2)
            })
            
        return jsonify({"error": "Invalid model response format"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500