import django
import os
import csv

case_csv = os.path.join(os.path.curdir, 'data', 'time_series_covid19_confirmed_global.csv')
death_csv = os.path.join(os.path.curdir, 'data', 'time_series_covid19_deaths_global.csv')


def update_csv_files():
    pass


def load_csv(path:str):
    with open(path,'r') as file:
        dr = csv.DictReader(file)
        return [row for row in dr]


def process_rows(rows: list, is_cases: bool):
    for row in rows:
        # Every row contains location data (country/prov), and a list of dates mapping to numbers
        base_row = {
            'region': row['Province/State'],
            'parent_region': row['Country/Region']
        }

        if base_row['parent_region'] and not base_row['region']:
            base_row['region'] = base_row['parent_region']
            base_row['parent_region'] = None

        for key in row.keys():
            if str(key).count("/") == 2:
                base_row['date'] = str(key)
                base_row['value'] = row[key]
                business.process_row(base_row, is_cases)


def main():

    #case_rows = load_csv(case_csv)
    #process_rows(case_rows,True)

    death_rows = load_csv(death_csv)
    process_rows(death_rows, False)


if __name__ == '__main__':
    print('Getting latest Covid Data')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mortality.settings')
    django.setup()

    import covid.business as business

    main()
