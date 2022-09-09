import pandas as pd
import pathlib
from mongo_helper import get_database, read_mongo
import json
import re
import glob
from datetime import datetime
from openpyxl import load_workbook


def parse_ergo_from_excel(excel_path, column_range='J:AO', date_column='E1', collection_name='player_ergo'):
    db = get_database()
    collection = db.get_collection(collection_name)

    cur_df = pd.read_excel(excel_path, sheet_name='Данные', usecols=column_range)
    cur_df = cur_df.drop([0])
    cur_df.dropna(how='all', inplace=True)
    file_name = pathlib.Path(excel_path).stem
    # if len(file_name) > 55:
    #     season_part = 1
    # else:
    #     season_part = 2
    # get date from excel

    wb = load_workbook(excel_path, data_only=True)
    sh = wb["Данные"]
    date = datetime.strptime(sh[date_column].value, '%d.%m.%Y')
    if date.month in [6, 7, 8, 9]:
        season_part = 1
    else:
        season_part = 2

    print(file_name, season_part)
    name = re.search(r".+?(\d+).+?(\d{4}-\d{4}).+", file_name)
    if name:
        player = 'X' + name.group(1)
        season = name.group(2)
        cur_df['player'] = player
        cur_df['season'] = season
        cur_df['season_part'] = season_part
    else:
        assert print('Invalid player')

    records = json.loads(cur_df.T.to_json()).values()
    collection.insert_many(records)


for file_path in glob.glob('d:/ITMO/Hackathon/raw_data/**/*.xlsx', recursive=True):
    parse_ergo_from_excel(file_path)
