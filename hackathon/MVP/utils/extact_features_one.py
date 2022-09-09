import pandas as pd
import numpy as np
import datetime


def prepare_data (data_path):
    data = pd.read_csv(data_path,encoding='utf-8',index_col=0)
    
    data.drop(columns = ['Маркер', 'Комн. Темп.', ], inplace = True)
    data.drop(columns = ['SpO2'], inplace = True)
    
    data[['ЧСС', 'VO2/HR','Revolution', 'Power', 'Фаза']]=\
        data[['ЧСС', 'VO2/HR','Revolution', 'Power', 'Фаза']].fillna(method = 'ffill')
    data[['P Сист.','P. диастол.']] = data[['P Сист.','P. диастол.']].fillna(method = 'bfill').fillna(method = 'ffill')
    
    data['t'] = pd.to_datetime(data['t'])
    
    column_not_series = ['Revolution','P Сист.','P. диастол.','Фаза']
    series_column = [x for x in list(data.columns) if x not in [*column_not_series,'season','season_part','player','t']]
    
    return data, column_not_series, series_column


def get_anomalies(series,column, win_size, sigma_val=1.96):   
    series = series[['t',column]].set_index('t')
    
    rolling_mean = series.rolling(window=win_size).mean()

    std = np.std(series[win_size:] - rolling_mean[win_size:])
    lower_bond = rolling_mean - (sigma_val * std)
    upper_bond = rolling_mean + (sigma_val * std)

    anomalies = pd.DataFrame(index=series.index, columns=series.columns)
    anomalies[series<lower_bond] = series[series<lower_bond]
    anomalies[series>upper_bond] = series[series>upper_bond]
    
    return anomalies


def get_feature_from_anom(anomalies, column):
    anomalies = anomalies[anomalies.isna()[column] != True]
    return anomalies.count()[0], anomalies.mean()[0], anomalies.min()[0],anomalies.max()[0]


def generate_features(data,series_column):
    one_player_features = []
    
    for column in series_column:
        anomalies = get_anomalies(data,column,5)
        features = get_feature_from_anom(anomalies, column)
        one_player_features.extend(features)
        
    return one_player_features


def extract_features(data_path):
    data, column_not_series, series_column = prepare_data(data_path)
    
    one_player_features = generate_features(data,series_column)  
    data_new = pd.DataFrame(one_player_features)
    
    return data, data_new, column_not_series, series_column


if __name__ == '__main__':
    
    #data - обработанные данные (заполнены пропуски, удалены ненужные колонки)
    #data_new - нагенеренные фичи, но без 4 колонок: 'Revolution','P Сист.','P. диастол.','Фаза'
    # тк они не являются временными рядами (или константа или линейная зависимость)
    # column_not_series - названия колонок: 'Revolution','P Сист.','P. диастол.','Фаза'
    # series_column - остальные названия колонок, по которым были нагенерены фичи
    data_path = input()
    data, data_new, column_not_series, series_column = extract_features(data_path)
    data_new.to_csv('data_new_one_player.csv')