import openpyxl as xl
import pandas as pd
import glob
import pathlib


# columns=['t', 'Rf', 'VT', 'VE_ergo', 'IV', 'VO2', 'VCO2', 'RQ', 'O2exp', 'CO2exp', 'VE/VO2',
#                            'VE/VCO2', 'VO2/Kg', 'METS', 'ЧСС', 'VO2/HR', 'FeO2', 'FeCO2', 'FetO2', 'FetCO2', 'FiO2',
#                            'FiCO2', 'PeO2', 'PeCO2', 'PetO2', 'PetCO2', 'SpO2', 'Power', 'Revolution', 'P Сист.',
#                            'P. диастол.', 'Фаза', 'Маркер', 'Комн. Темп.', 'RH Amb', 'Давление датчик.', 'PB', 'EEkc',
#                            'EEh', 'EEm', 'EEtot', 'EEkg', 'PRO', 'FAT', 'CHO', 'PRO%', 'FAT%', 'CHO%', 'npRQ',
#                            'GPS Дист.', 'ST I', 'ST II', 'ST III', 'ST aVR', 'ST aVL', 'ST aVF', 'ST V1', 'ST V2',
#                            'ST V3', 'ST V4', 'ST V5', 'ST V6', 'S I', 'S II', 'S III', 'S aVR', 'S aVL', 'S aVF',
#                            'S V1', 'S V2', 'S V3', 'S V4', 'S V5', 'S V6', 'Ti', 'Te', 'Ttot', 'Ti/Ttot', 'VD/VT e',
#                            'LogVE', 't Rel', 'марк. Скорость', 'mark Dist.', 'DP', 'Время фазы', 'VO2%Pred',
#                            'VO2/Kg%Pred', 'BR', 'VT/Ti', 'HRR', 'PaCO2_e', 'SV', 'CO']

df = pd.DataFrame()

for file_path in glob.glob('d:/ITMO/Hackathon/сезон*/*.xlsx', recursive=True):
    file_name = pathlib.Path(file_path).stem
    cur_df = pd.read_excel(file_path, sheet_name='Данные', usecols='J:AO')
    cur_df = cur_df.drop([0])
    cur_df.dropna(how='all', inplace=True)
    if len(file_name.split()) == 3:
        player, season = file_name.split()[:2]
        season_part = 2
    else:
        player, season = file_name.split()
        season_part = 1

    cur_df['player'] = player
    cur_df['season'] = season
    cur_df['season_part'] = season_part
    df = pd.concat([df, cur_df], ignore_index=True)

df = df.drop([0])
df.to_csv('d:/ITMO/Hackathon/data/all_seasons.csv', encoding='utf8')

pass
