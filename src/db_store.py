#Importing necessary libraries
from pymongo import MongoClient

"""
Function to store data in MongoDB.
Args:
    data (dict or list): The data to be stored in MongoDB. It can be a single document or a list of documents.
    db_name (str): The name of the database where the data will be stored.
    collection_name (str): The name of the collection where the data will be stored.
    uri (str): The MongoDB connection URI.
"""

def store_to_mongo(data, db_name, collection_name , uri):
    
    # Connect to MongoDB
    print("🔗 Connecting to MongoDB...")
    client = MongoClient(uri)

    # Access the database
    db = client[db_name]

    # Access the collection
    collection = db[collection_name]

    # Insert the data into the collection
    if isinstance(data, list):
        # If data is a list, insert multiple documents
        result = collection.insert_many(data)
    else:
        # If data is a single document, insert one document
        result = collection.insert_one(data)
    print(f"✅ Saved {len(data) if isinstance(data, list) else 1} documents in MongoDB.")

    client.close()  # Close the connection to MongoDB
    print("🔗 Connection to MongoDB closed.")