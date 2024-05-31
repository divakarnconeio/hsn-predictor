import pandas as pd
from pymongo import MongoClient
import ast
from dotenv import load_dotenv

load_dotenv()

import os

# Load environment variables
MONGODB_URI = os.getenv('MONGODB_URI')

# MongoDB connection
client = MongoClient(MONGODB_URI)
db = client['hsn_database']
collection = db['hsn_embeddings']

# Read CSV data
csv_file = 'HSN_TAGS_database.csv'
df = pd.read_csv(csv_file)


# Function to convert string representation of list to actual list
def str_to_list(embedding_str):
    try:
        # Try using ast.literal_eval for standard list strings
        return ast.literal_eval(embedding_str)
    except (ValueError, SyntaxError):
        # Fallback for space-separated or other formatted strings
        embedding_str = embedding_str.strip('[]')
        return [float(x) for x in embedding_str.split()]

# Insert data into MongoDB
def insert_hsn_data(df):
    
    for index, row in df.iterrows():
        hsn_number = row['HSN']
        tags = row['Tags']
        embedding = str_to_list(row['embedding'])

        hsn_data = {
            'hsn_number': hsn_number,
            'tags': tags,
            'embedding': embedding
        }
        collection.insert_one(hsn_data)

    print('Data inserted successfully')


insert_hsn_data(df)
        

