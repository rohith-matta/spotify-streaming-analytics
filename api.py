from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)  # This enables CORS for all routes

def get_top_data(collection_name, group_field, limit=10):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["music_streaming"]
    collection = db[collection_name]
    pipeline = [
        {"$group": {"_id": f"${group_field}", "total_count": {"$sum": "$count"}}},
        {"$sort": {"total_count": -1}},
        {"$limit": limit}
    ]
    results = list(collection.aggregate(pipeline))
    client.close()
    return [{"name": doc["_id"], "count": doc["total_count"]} for doc in results]

@app.route('/api/top-songs', methods=['GET'])
def top_songs():
    data = get_top_data("aggregated_results_songs", "track_name")
    return jsonify(data)

@app.route('/api/top-artists', methods=['GET'])
def top_artists():
    data = get_top_data("aggregated_results_artists", "artist_name")
    return jsonify(data)

@app.route('/', methods=['GET'])
def home():
    return "API is running", 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
