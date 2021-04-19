from hdx.hdx_configuration import Configuration
from hdx.data.dataset import Dataset
import pandas as pd
import numpy as np
import csv
from zipfile import ZipFile
import os
from utilities import download_url
import subprocess


class LiveMobility:
    def __init__(self):
        self.url = None
        self.file_name = None
        self.data = None

    def get_url(self):
        Configuration.create(hdx_site='prod',
                             user_agent='A_Quick_Example',
                             hdx_read_only=True)
        dataset = Dataset.read_from_hdx('movement-range-maps')
        resources = dataset.get_resources()
        dic = resources[1]
        self.url = dic['download_url']
        return self

    def get_file(self):
        self.file_name = "../data/prediction/mvt_range.zip"
        download_url(self.url, self.file_name)
        return self

    def unzipp(self):
        with ZipFile(self.file_name, 'r') as zip:
            # printing all the contents of the zip file
            zip.printdir()

            # extracting all the files
            print('Extracting mv_range file now...')
            mvt_range = zip.namelist()[-1]
            zip.extract(mvt_range)
            print('Done!')

        os.system("""grep "FRA" """ + mvt_range +
                  """ > mouvement-range-FRA.txt""")
        os.system("""head -n 1 """ + mvt_range + """ >> header.txt""")
        os.system(
            """cat header.txt mouvement-range-FRA.txt >mouvement-range-FRA-final.txt"""
        )
        return self

    def process_mobility(self):
        mvt_range_final = "mouvement-range-FRA-final.txt"

        with open(mvt_range_final) as f:
            reader = csv.reader(f, delimiter="\t")
            d = list(reader)

        data_mob = pd.DataFrame(d[1:], columns=d[0])
        data_mob = data_mob[data_mob['country'] == 'FRA']

        #get df with latest data for all regions
        data_mob = data_mob[data_mob['ds'] == list(data_mob.iloc[[-1]]['ds'])
                            [0]][[
                                'ds', 'polygon_name',
                                'all_day_bing_tiles_visited_relative_change',
                                'all_day_ratio_single_tile_users'
                            ]]

        prediction_data = pd.read_csv(
            '../data/train/pop/fr/departements-francais.csv', sep=';')
        prediction_data.columns = [
            'dep_num', 'name', 'region', 'capital', 'area', 'total', 'density'
        ]
        prediction_data = prediction_data.sort_values('dep_num')
        prediction_data = prediction_data[:-5]
        prediction_data['region'] = prediction_data['region'].replace(
            {'Ile-de-France': 'Île-de-France'})

        prediction_data['stay_put'] = 0.0
        prediction_data['go_out'] = 0.0


def add_go_out(row):
    region = row['region']
    go_out = data_mob[data_mob['polygon_name'] ==
                      region]['all_day_bing_tiles_visited_relative_change']
    return float(list(go_out)[0])


def add_stay_put(row):
    region = row['region']
    stay_put = data_mob[data_mob['polygon_name'] ==
                        region]['all_day_ratio_single_tile_users']
    return float(list(stay_put)[0])


prediction_data['go_out'] = prediction_data.apply(add_go_out, axis=1)
prediction_data['stay_put'] = prediction_data.apply(add_stay_put, axis=1)

prediction_data.to_csv('../data/prediction/prediction_data.csv', index=False)
