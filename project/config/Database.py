import pymongo
import os

try:
    db_connection = os.getenv("DATABASE_URL")
    client = pymongo.MongoClient(db_connection)
    db = client.nlp_api
    print("SUCCESS CONNECT TO DB")
except Exception as ex:
    print('ERROR CONNECT TO MONGODB')
    print(ex)
