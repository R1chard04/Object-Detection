# this is a constant file that get all the environment variables
# import libraries
import os

from dotenv import load_dotenv
load_dotenv()

username = os.getenv('MONGO_DB_USERNAME')
password = os.getenv('MONGO_DB_PASSWORD')
