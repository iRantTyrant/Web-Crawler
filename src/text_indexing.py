from pymongo import MongoClient, TEXT
from bson import json_util
import re

"""
This function creates a text index on the 'title' and 'content' fields of a MongoDB collection,
allows the user to search for documents using a text search query, and optionally saves the results to a JSON file.
It drops any existing text index before creating a new one.
Args:
    user_index (str): The search term provided by the user. If None, a default search term is used.
    uri (str): The MongoDB connection URI.
    db_name (str): The name of the database.
    collection_name (str): The name of the collection to index and search.
"""

def create_text_index_and_search(user_index, uri, db_name, collection_name):

    #Connect to MongoDB
    print("🔗 Connecting to MongoDB...")
    client = MongoClient(uri)
    db = client[db_name]
    collection = db[collection_name]

    #List to save the indexed documents
    results_list = []

    # Drop ONLY existing text index (not all indexes)
    for name, index in collection.index_information().items():
        if index.get('weights'):  # Detects text index
            print(f"Dropping existing text index: {name}")
            collection.drop_index(name)

    # Create a text index on the 'title' and 'content' fields
    collection.create_index([
        ("title", TEXT),
        ("content", TEXT),
    ])

    # Ask the user for a search term
    if (user_index):
        # User provided search term
        search_query = user_index  
    else:
        # Default search term
        search_query = '"deep dive" decompression' 

    # Print the search query
    print(f"Searching for: {search_query}")

    # Search the collection using the text index
    results = collection.find(
        { "$text": { "$search": search_query } },
        { "score": { "$meta": "textScore" }, "title": 1, "content": 1 , "link": 1 }
    ).sort([("score", {"$meta": "textScore"})])

    # Εκτύπωση αποτελεσμάτων
    found = False
    for result in results:
        found = True
        results_list.append(result)#append the result to the list that will be saved to the json file
        print(f"Title: {result.get('title')}")
        print(f"Link: {result.get('link')}")
        print("Excerpt:")
        print(result.get("content", "")[:300] + "...\n")
        print("-" * 80)

    #In case there are no results, we will print a message    
    if not found:
        print("No results found.")

    #Ask the user if they want to save the results into json files
    save_choice = input("Do you want to save the results into a JSON file? (yes/no): ").strip().lower()

    #Save the results to a JSON file
    if save_choice == 'yes':

        # Ensure the search query is safe for filenames
        safe_query = re.sub(r'\W+', '_', search_query)

        # Create a filename based on the search query
        filename = f'produced_json_files/indexed_search_results_{safe_query}.json'
        
        # Write the results to a JSON file
        with open(filename, 'w') as f:
            f.write(json_util.dumps(results_list, indent=4))

        # Print the filename where results are saved
        print(f"Results saved to {filename}")
    #If the index didnt find any results, we will not save the results to a file
    else:
        print("Results not saved to a file.")
    client.close()  # Close the connection to MongoDB
    print("🔗 Connection to MongoDB closed.")
