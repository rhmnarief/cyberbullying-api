import pymongo
import os

try:
    db_connection = os.getenv("DATABASE_URL")
    client = pymongo.MongoClient(db_connection)
    db = client.nlp_api
    print("SUCCESS CONNECT TO DB")
    client.server_info()  # trigger exeception if cannot connect to db
except Exception as ex:
    print('ERROR CONNECT TO MONGODB')
    print(ex)
