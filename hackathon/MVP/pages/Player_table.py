import os.path

import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
import pandas as pd
import pymongo as mongo
from PIL import Image
import matplotlib.pyplot as plt
import json


default_image = 'd:/Projects/hackathon/MVP/photo/scrosby.jpg'


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

    if not cursor:
        return
    # Expand the cursor and construct the DataFrame
    df = pd.DataFrame(list(cursor))
    # Delete the _id
    if no_id:
        del df['_id']
    return df


def aggrid_interactive_table(df: pd.DataFrame, columns=[]):
    """Creates an st-aggrid interactive table based on a dataframe.
    Args:
        df (pd.DataFrame]): Source dataframe
    Returns:
        dict: The selected row
    """
    options = GridOptionsBuilder.from_dataframe(
        df[columns], enableRowGroup=True, enableValue=True, enablePivot=True
    )

    options.configure_side_bar()

    options.configure_selection("multiple")
    options.configure_pagination(paginationAutoPageSize=False, paginationPageSize=5)

    selection = AgGrid(
        df,
        enable_enterprise_modules=True,
        gridOptions=options.build(),
        theme="streamlit",
        update_mode=GridUpdateMode.MODEL_CHANGED,
        allow_unsafe_jscode=True,
    )

    return selection


def plot_series(series, columns):
    # plt.figure(figsize = (20,9))
    series = series.copy()
    series['t'] = pd.to_datetime(series['t'])
    fig, ax = plt.subplots(len(columns), 1)
    for i, column in enumerate(columns):
        ax[i].plot(series['t'], series[column])
        # ax.grid(True)
        # ax.xlabel('Time')
        # ax.ylabel(column)
    return fig


def plot_series_against_top(series, df_top, columns):
    plt.figure(figsize=(20, 9))
    series = series.copy()
    df_top = df_top.copy()
    series['t'] = pd.to_datetime(series['t'])
    df_top['t'] = pd.to_datetime(df_top['t'])

    series['t'] -= series['t'].iloc[0]
    df_top['t'] -= df_top['t'].iloc[0]

    fig, ax = plt.subplots(len(columns), 1)
    for i, column in enumerate(columns):
        ax[i].plot(series['t'], series[column])
        ax[i].plot(df_top['t'], df_top[column])
        ax[i].grid(True)
        ax[i].set_xlabel('Time')
        ax[i].set_ylabel(column)
    return fig


def plot_series_against_each_other(ergos, columns):
    plt.figure(figsize=(20, 9))
    for ergo in ergos:
        ergo['t'] = pd.to_datetime(ergo['t'])
        ergo['t'] -= ergo['t'].iloc[0]

    fig, ax = plt.subplots(len(columns), 1)
    for i, column in enumerate(columns):
        for ergo in ergos:
            ax[i].plot(ergo['t'], ergo[column], label='temp')

        ax[i].grid(True)
        ax[i].set_xlabel('Time')
        ax[i].set_ylabel(column)
    return fig


db = get_database()
st.title("Таблица игроков")
df = read_mongo(db, 'players_res')
df_ergo_top = read_mongo(db, 'player_ergo', query={'player': 'X61', 'season': '2020-2021', 'season_part': 1})
selection = aggrid_interactive_table(df=df, columns=['player', 'season', 'result'])
ergo_cols = ['VO2', 'VCO2', 'RQ', 'O2exp']


if selection and len(selection["selected_rows"]):
    st.write("You selected:")
    col1, col2 = st.columns([1, 3])
    image_path = f'd:/Projects/hackathon/MVP/photo/{selection["selected_rows"][0]["player"]}.png'
    if os.path.exists(image_path):
        image = Image.open(image_path)
    else:
        image = Image.open(default_image)
    col1.image(image)
    age = selection["selected_rows"][0]["age"]
    position = selection["selected_rows"][0]["position"]
    player = selection["selected_rows"][0]["player"]

    col2.write({"Возраст: ": age,
                "Позиция": position})

    # series = df[df['player'] == player]

    if len(selection["selected_rows"]) == 1:
        df_ergo = read_mongo(db, 'player_ergo', query={'player': player, 'season': '2020-2021', 'season_part': 1})
        col2.pyplot(plot_series_against_top(df_ergo, df_ergo_top, ergo_cols))
    else:
        col2.write(len(selection["selected_rows"]))
        ergos = []
        for row in selection["selected_rows"]:
            cur_player = row['player']
            df_ergo = read_mongo(db,
                                 'player_ergo', query={'player': cur_player, 'season': '2020-2021', 'season_part': 1})
            ergos.append(df_ergo)

        col2.pyplot(plot_series_against_each_other(ergos, ergo_cols))
