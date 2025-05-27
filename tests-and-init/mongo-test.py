from pymongo import MongoClient

client = MongoClient("mongodb://mongoadmin:secret123@localhost:27017/")
db = client["web_data"]
print(db.list_collection_names())