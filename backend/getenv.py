# this is a constant file that get all the environment variables
# import libraries
import os

from dotenv import load_dotenv
load_dotenv()

# getting mongodb connection credentials
mongodb_username = os.getenv('MONGO_DB_USERNAME')
mongodb_password = os.getenv('MONGO_DB_PASSWORD')

# getting mysql connection credentials
mysql_username = os.getenv('MYSQL_DB_USERNAME')
mysql_password = os.getenv('MYSQL_DB_PASSWORD')
