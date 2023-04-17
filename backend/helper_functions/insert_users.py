# insert the users and permissions to MongoDB Cluster
# import libraries
from flask import Flask
from flask_pymongo import pymongo

# import other files
from app import app
from getenv import username, password

CONNECTION_STRING = f'mongodb+srv://{username}:{password}@cluster0.cyuaazi.mongodb.net/?retryWrites=true&w=majority'

# create a mongodb client
client = pymongo.MongoClient(CONNECTION_STRING)
mongo_db = client.get_database('Martinrea')

# get the collections inside the database
users_collection = pymongo.collection.Collection(mongo_db, 'Users')
permissions_collection = pymongo.collection.Collection(mongo_db, 'Permissions')


