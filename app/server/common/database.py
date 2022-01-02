from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

database = client.rsa

user_collection = database.get_collection("users")

image_collection = database.get_collection("images")

