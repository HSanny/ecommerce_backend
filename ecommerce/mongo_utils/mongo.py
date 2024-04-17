from pymongo import MongoClient

# This module provides a function to establish a connection to MongoDB using PyMongo. 
# MongoClient is initialized with the MongoDB URI (in this case, pointing to a local MongoDB instance running on port 27017). 
# db_handle is a reference to the database (ecommerce). 
# This function returns two values: the database handle (db_handle) which you use to interact with the database, and the client object which represents the MongoDB client connection.

def get_db_handle():
    db_name = "ecommerce"
    # host = "localhost"
    # port = 27017
    # username = None
    # password = None
    # Replace the URI below with MongoDB Atlas connection string
    uri = "mongodb+srv://synhong43:sanny37567269@cluster0.suhnds0.mongodb.net/?retryWrites=true&w=majority&appName=cluster0"
    
    # client = MongoClient(
    #     host=host,
    #     port=port,
    #     username=username,
    #     password=password,
    # )
    client = MongoClient(uri)
    db_handle = client[db_name]
    return db_handle, client