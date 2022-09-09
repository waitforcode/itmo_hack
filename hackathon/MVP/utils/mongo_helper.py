import pymongo as mongo
import pandas as pd


def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    uri = "mongodb://localhost:27017"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = mongo.MongoClient(uri)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['players_db']


def read_mongo(db, collection, query={}, no_id=True):
    """ Read from Mongo and Store into DataFrame """
    # Make a query to the specific DB and Collection
    cursor = db[collection].find(query)

    # Expand the cursor and construct the DataFrame
    df = pd.DataFrame(list(cursor))
    # Delete the _id
    if no_id:
        del df['_id']
    return df