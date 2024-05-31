from flask import Flask, request, jsonify
from pymongo import MongoClient
import numpy as np
from bson import ObjectId
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")

load_dotenv()

import os
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Load environment variables
MONGODB_URI = os.getenv('MONGODB_URI')

app = Flask(__name__)

# MongoDB connection
client = MongoClient(MONGODB_URI)
db = client['hsn_database']
collection = db['hsn_embeddings']

# Helper function to convert vector to list (for JSON serialization)
def vector_to_list(vector):
    return vector.tolist()

# Helper function to convert list to vector (for similarity calculation)
def list_to_vector(lst):
    return np.array(lst)

@app.route('/')
def home():
    return 'Welcome to the HSN Search API'

@app.route('/add_hsn', methods=['POST'])
def add_hsn():
    data = request.json
    hsn_number = data['hsn_number']
    description = data['description']
    embedding = data['embedding']  # Assume embedding is a list of floats

    # Insert HSN data into MongoDB
    hsn_data = {
        'hsn_number': hsn_number,
        'description': description,
        'embedding': embedding
    }
    result = collection.insert_one(hsn_data)
    
    return jsonify({'message': 'HSN added successfully', 'id': str(result.inserted_id)}), 201

@app.route('/search_hsn', methods=['POST'])
def search_hsn():
    data = request.json
    query_embedding = list_to_vector(data['embedding'])

    # Retrieve all HSN entries
    hsn_entries = list(collection.find())

    # Calculate similarities
    results = []
    for entry in hsn_entries:
        hsn_embedding = list_to_vector(entry['embedding'])
        similarity = cosine_similarity([query_embedding], [hsn_embedding])[0][0]
        results.append({
            'hsn_number': entry['hsn_number'],
            'description': entry['description'],
            'similarity': similarity
        })

    # Sort results by similarity
    results.sort(key=lambda x: x['similarity'], reverse=True)
    
    # Return the first 10 entries
    return jsonify(results[:10]), 200


@app.route('/search_description', methods=['POST'])
def search_description():
    data = request.json
    query = data.get('description')

    if not query:
        return jsonify({'error': 'No description provided'}), 400

    try:
        # Encode query
        query_embedding = model.encode(query).tolist()

        # Define the vector search query
        search_query = [
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "path": "embedding",
                    "queryVector": query_embedding,
                    "numCandidates": 10,
                    "limit": 10
                }
            }
        ]

        # Perform the vector search
        results = list(collection.aggregate(search_query))
        # logging.debug(f"Search results: {results}")

            # Format the results
        formatted_results = []
        for result in results:
            formatted_results.append({
                'hsn_number': result['hsn_number'],
            })

        # Return the results
        logging.debug(f"formatted results: {formatted_results}")
        return jsonify(formatted_results), 200
        

    except Exception as e:
        logging.error(f"Error during search: {e}")
        return jsonify({'error': 'An error occurred during the search'}), 500




if __name__ == '__main__':
    app.run(debug=True)
