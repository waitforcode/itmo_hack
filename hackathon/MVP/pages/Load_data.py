import streamlit as st
import pandas as pd
import pymongo as mongo
import json


def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    uri = "mongodb://localhost:27017"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = mongo.MongoClient(uri)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client['players_db']


db = get_database()
data = st.file_uploader('Загрузите данные велоэргометрии', type=["csv", "xlsx"])
if data is not None:
    df = pd.read_csv(data, sep=';')
    collection = db.get_collection('players_res')
    records = json.loads(df.T.to_json()).values()
    collection.insert_many(records)
