from pymongo import MongoClient

client = MongoClient(
    host = 'mongodb://localhost:27017/', # <-- IP and port go here
    serverSelectionTimeoutMS = 3000, # 3 second timeout
    username="root",
    password="example",
)

server_info = client.server_info()
print (server_info)

databases = client.list_database_names()
print("Databases:", databases)

dblist = client.list_database_names()
if "mydatabase" in dblist:
  print("The database exists.")