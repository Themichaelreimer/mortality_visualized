from django.core.management.base import BaseCommand, CommandError
from hmd.models import *

import os
from typing import List, Tuple

FILE_NAMES = ['fltper_1x1.txt', 'mltper_1x1.txt']


def extract_row(text: str) -> list:
    return [x for x in text.split(' ') if x]


def get_sex(text: str) -> str:
    ''' returns m or f based on input, which should be a file name '''
    if "flt" in text:
        return 'f'
    if 'mlt' in text:
        return 'm'


class Command(BaseCommand):
    help = 'Loads HMD life tables into database. Calculates cumulative along the way'

    def handle(self, *args, **options):
        path = os.path.join('data', 'hmd_countries') # Next is country, then 'STATS', then FILE_NAME
        folders = os.listdir(path)
        for folder in folders:
            for file_name in FILE_NAMES:

                file_path = os.path.join(path, folder, 'STATS', file_name)

                if os.path.isfile(file_path):
                    try:
                        self.process_life_table(file_path, str(folder))
                    except Exception as e:
                        print(f'type({e}) - {e}')

    def process_life_table(self, path, short_name: str):
        with open(path, "r") as file:
            rows = file.readlines()
            country_name = rows[0].split(',')[0]
            country = self.ensure_country(country_name, short_name)
            sex = get_sex(path)

            for row_text in rows[4:]:
                row = extract_row(row_text)
                year = row[0]
                age = row[1]

                probability = row[3]
                if probability == '.':
                    probability = 100

                if row[5] == '.':
                    p_alive = 0
                else:
                    p_alive = int(row[5])/100000

                if '+' in age:
                    age = age[0:-1]

                params = {
                    'country': country,
                    'sex': sex,
                    'year': year,
                    'age': age,
                    'probability': probability,
                    'cumulative_probability': p_alive
                }

                self.ensure_life_table_entry(params)

    @staticmethod
    def ensure_country(country: str, short: str) -> Country:
        res, _ = Country.objects.get_or_create(name=country, short_name=short)
        return res

    @staticmethod
    def ensure_life_table_entry(params: dict):
        '''
        Takes: country,sex,age,year,probability,cumulative_probability
        :param params: dict with the above keys
        :return: None
        '''
        LifeTable.objects.get_or_create(**params)


