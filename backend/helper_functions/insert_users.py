# insert the users and permissions to MongoDB Cluster
# import libraries
from flask import Flask
from flask_pymongo import pymongo

# import other files
from getenv import mongodb_username, mongodb_password

CONNECTION_STRING = f"mongodb+srv://{mongodb_username}:{mongodb_password}@martinreahfs.lgbfiq1.mongodb.net/?retryWrites=true&w=majority"

# create a mongodb client
client = pymongo.MongoClient(CONNECTION_STRING)
mongo_db = client.get_database('Martinrea_HFS')

# get the collections inside the database
users_collection = pymongo.collection.Collection(mongo_db, 'Users')


