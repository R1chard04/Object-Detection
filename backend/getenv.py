# this is a constant file that get all the environment variables
# import libraries
import os

from dotenv import load_dotenv
load_dotenv()

# getting mongodb connection credentials
mongodb_username = os.getenv('MONGO_DB_USERNAME', "mongodb username does not exist")
mongodb_password = os.getenv('MONGO_DB_PASSWORD', "mongodb password does not exist")

# getting mysql connection credentials
mysql_username = os.getenv('MYSQL_DB_USERNAME', "mysql username does not exist")
mysql_password = os.getenv('MYSQL_DB_PASSWORD', "mysql password does not exist")
mysql_host = os.getenv('MYSQL_DB_HOST', "mysql host does not exist")
mysql_port = os.getenv('MYSQL_DB_PORT', "mysql port does not exist")
mysql_db_name = os.getenv('MYSQL_DB_NAME', "mysql database name does not exist")
