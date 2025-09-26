# app.py
import os
import pickle
import re
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId

# --- Initialization ---
app = Flask(__name__)
CORS(app)

# --- AI Model Class ---
class LogClassifier:
    def __init__(self):
        self.keywords = ["error", "failed", "exception", "timeout"]

    def predict(self, log_message):
        log_message = log_message.lower()
        for keyword in self.keywords:
            if keyword in log_message:
                return "anomaly"
        return "normal"

# --- Load model safely ---
try:
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    print("AI Model loaded successfully.")
except Exception as e:
    print(f"Error loading model.pkl: {e}")
    model = LogClassifier()  # fallback to fresh instance

# --- MongoDB Connection ---
def get_mongo_collection():
    MONGO_URI = os.environ.get("MONGO_URI")
    if not MONGO_URI:
        raise ValueError("MONGO_URI environment variable not set")
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client.log_ingestor_db
    collection = db.logs
    # test connection
    client.admin.command("ping")
    return collection

try:
    logs_collection = get_mongo_collection()
    print("MongoDB connected successfully!")
except Exception as e:
    print(f"Could not connect to MongoDB: {e}")
    logs_collection = None  # allow app to start for deployment

# --- API Endpoints ---

@app.route("/ingest", methods=["POST"])
def ingest_log():
    if logs_collection is None:
        return jsonify({"error": "Database not connected"}), 500

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    logs_to_insert = []
    log_entries = data if isinstance(data, list) else [data]

    for log in log_entries:
        if "message" not in log:
            continue
        prediction = model.predict(log["message"])
        log["prediction"] = prediction
        if "timestamp" in log:
            log["timestamp"] = datetime.fromisoformat(log["timestamp"].replace("Z", "+00:00"))
        logs_to_insert.append(log)

    if logs_to_insert:
        logs_collection.insert_many(logs_to_insert)

    return jsonify({"status": "success", "ingested": len(logs_to_insert)}), 200

@app.route("/logs", methods=["GET"])
def get_logs():
    if logs_collection is None:
        return jsonify({"error": "Database not connected"}), 500

    query = {}
    if "message" in request.args and request.args["message"]:
        query["message"] = {"$regex": re.compile(request.args["message"], re.IGNORECASE)}

    date_filter = {}
    if "startDate" in request.args and request.args["startDate"]:
        date_filter["$gte"] = datetime.fromisoformat(request.args["startDate"].replace("Z", "+00:00"))
    if "endDate" in request.args and request.args["endDate"]:
        date_filter["$lte"] = datetime.fromisoformat(request.args["endDate"].replace("Z", "+00:00"))
    if date_filter:
        query["timestamp"] = date_filter

    for key, value in request.args.items():
        if value and key not in ["message", "startDate", "endDate"]:
            if key.startswith("metadata."):
                query[key] = value
            else:
                query[key] = {"$regex": re.compile(value, re.IGNORECASE)}

    try:
        results = list(logs_collection.find(query).sort("timestamp", -1))
        for result in results:
            result["_id"] = str(result["_id"])
            if "timestamp" in result:
                result["timestamp"] = result["timestamp"].isoformat()
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/logs/<log_id>", methods=["DELETE"])
def delete_log(log_id):
    if logs_collection is None:
        return jsonify({"error": "Database not connected"}), 500
    try:
        result = logs_collection.delete_one({"_id": ObjectId(log_id)})
        if result.deleted_count == 1:
            return jsonify({"status": "success", "message": "Log deleted"}), 200
        else:
            return jsonify({"status": "error", "message": "Log not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Main ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
