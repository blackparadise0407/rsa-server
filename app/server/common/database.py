from os import getenv

from pymongo import MongoClient

mongo_uri = getenv("MONGO_URI", "mongodb://localhost:27017/")

database_name = getenv("DATABASE_NAME", "rsa")

client = MongoClient(mongo_uri)

database = client[database_name]

user_collection = database.get_collection("users")

image_collection = database.get_collection("images")

shared_image_collection = database.get_collection("shared_images")

