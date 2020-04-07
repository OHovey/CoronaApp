import pandas as pd
import csv
import datetime
from datetime import date, timedelta
import requests
import sqlite3
import os
from operator import itemgetter

from promise import Promise 
from promise.dataloader import DataLoader


file_headers = {
    0: {'headers': ['ï»¿Province/State',
        'Country/Region',
        'Last Update',
        'Confirmed',
        'Deaths',
        'Recovered'], 'index_array': { 'country': 1, 'province': 0, 'confirmed': 3, 'deaths': 4, 'recovered': 5 }},
    1: {'headers': ['Province/State',
        'Country/Region',
        'Last Update',
        'Confirmed',
        'Deaths',
        'Recovered'], 'index_array': { 'country': 1, 'province': 0, 'confirmed': 3, 'deaths': 4, 'recovered': 5 }},
    2: {'headers': ['Province/State',
        'Country/Region',
        'Last Update',
        'Confirmed',
        'Deaths',
        'Recovered',
        'Latitude',
        'Longitude'], 'index_array': { 'country': 1, 'province': 0, 'confirmed': 3, 'deaths': 4, 'recovered': 5 }},
    3: {'headers': ['ï»¿Province/State',
        'Country/Region',
        'Last Update',
        'Confirmed',
        'Deaths',
        'Recovered',
        'Latitude',
        'Longitude'], 'index_array': { 'country': 1, 'province': 0, 'confirmed': 3, 'deaths': 4, 'recovered': 5 }},
    4: {'headers': ['Province/State',
        'Country/Region',
        'Last Update',
        'Confirmed',
        'Deaths',
        'Recovered',
        'Latitude',
        'Longitude'], 'index_array': { 'country': 1, 'province': 0, 'confirmed': 3, 'deaths': 4, 'recovered': 5 }},
    5: {'headers': ['ï»¿FIPS',
        'Admin2',
        'Province_State',
        'Country_Region',
        'Last_Update',
        'Lat',
        'Long_',
        'Confirmed',
        'Deaths',
        'Recovered',
        'Active',
        'Combined_Key'], 'index_array': { 'country': 3, 'province': 2, 'confirmed': 7, 'deaths': 8, 'recovered': 9 }},
    6: {'headers': ['FIPS',
        'Admin2',
        'Province_State',
        'Country_Region',
        'Last_Update',
        'Lat',
        'Long_',
        'Confirmed',
        'Deaths',
        'Recovered',
        'Active',
        'Combined_Key'], 'index_array': { 'country': 3, 'province': 2, 'last_update': 4, 'confirmed': 7, 'deaths': 8, 'recovered': 9 }}
}








def pullDownData():
    def fetch_it(days: int):
        current_date = date.today() - timedelta(days = days)
        request_url = f'https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-{current_date}.xlsx'
        r = requests.get(request_url, allow_redirects = True)
        open('covid.xls', 'wb').write(r.content)
    try:
        # try fetching todays data...
        fetch_it(0)
    except:
        # if todays' data doesn't exist, fetch yesterdays' data instead.
        fetch_it(1)
# https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-2020-03-23.xlsx





def convert_to_csv(filename: str):
    excel_data = pd.read_excel(filename, 'COVID-19-geographic-disbtributi', index_col = None) 
    print(excel_data.head())
    excel_data.to_csv('covid.csv', encoding = 'utf-8')


def delete_all_from_tables():
    sql = 'DELETE FROM country;' 
    sql2 = 'DELETE FROM country_history;' 

    conn = sqlite3.connect('covid.sqlite3') 
    c = conn.cursor() 
    c.execute(sql) 
    c.execute(sql2) 
    conn.commit() 
    conn.close()


def write_csv_data_to_database(filename):
    from models import engine, db_session, Country 
    with open(filename, 'r') as readfile:
        reader = csv.reader(readfile) 
        for index, row in enumerate(reader):
            print(f'row: {row}')
            if index == 0:
                continue
            if row[2] == '':
                row[2] = '0.0'

            try:
                country = Country(
                    name = row[0], 
                    total_cases = int(float(row[1])),
                    total_deaths = int(float(row[2])) 
                )
                db_session.add(country)

            except ValueError:
                country = Country(
                    name = row[0], 
                    total_cases = 0.0,
                    total_deaths = int(row[2]) 
                )
                db_session.add(country)

        db_session.commit()


def write_day_csv_data_to_database(filename):
    from models import engine, db_session, DayData, Country
    with open(filename, 'r') as readfile:
        reader = csv.reader(readfile) 
        for index, row in enumerate(reader):
            if index == 0:
                continue
            print(f'row: {row}')
            if index < 5:
                continue
            print(f'row[0]: {row[0]}')
            country = db_session.query(Country).filter_by(name = row[0]).first()
            date_data = [int(date_component) for date_component in row[1].split('-')]

            try:
                country_date = DayData(
                    country = country,
                    date = datetime.date(date_data[0], date_data[1], date_data[2]),
                    new_cases = int(row[2]),
                    new_deaths = int(float(row[3])),
                )
                print(f'country: {country_date.new_cases}')
                db_session.add(country_date)

            except ValueError:
                country_date = DayData(
                    country = country,
                    date = datetime.date(date_data[0], date_data[1], date_data[2]),
                    new_cases = int(row[2]),
                    new_deaths = 0
                )
                db_session.add(country_date)

        db_session.commit()


def alter_day_data(filename):
    with open(filename, 'r') as readfile:
        reader = csv.reader(readfile) 
        data_points = []
        for index, row in enumerate(reader):
            if index == 0:
                continue 
            if row[2] == '':
                row[2] = '0.0' 

            day_data = {
                'country_name': row[7],
                'date': row[1].split(',')[0],
                'new_cases': int(row[5]),
                'new_deaths': row[6] 
            }
            data_points.append(day_data)
        
        with open('day_data.csv', 'w', newline='') as writefile:
            writer = csv.writer(writefile)
            for day in data_points:
                writer.writerow(day.values()) 
            
        writefile.close() 

    readfile.close() 


def alter_data(filename): 
    with open(filename, 'r') as readfile: 
        reader = csv.reader(readfile) 
        last_location = ''
        total_cases = 0 
        total_deaths = 0

        countries = []

        for index, row in enumerate(reader):
            if index == 0: continue
            if row[4] == '': row[4] = 0

            if row[7] == last_location:
                try:
                    total_cases += int(float(row[5])) 
                    total_deaths += int(float(row[6]))
                except ValueError:
                    total_cases += 0 
                    total_deaths += int(row[6]) 
            else:
                country_data = {
                    'name': last_location,
                    'total_cases': total_cases,
                    'total_deaths': total_deaths
                }
                countries.append(country_data) 

                last_location = row[7] 
                try:
                    total_cases += int(float(row[5])) 
                    total_deaths += int(float(row[6]))
                except ValueError:
                    total_cases += 0 
                    total_deaths += int(row[6]) 
                
                total_cases = 0 
                total_deaths = 0
        
        with open('altered_covid.csv', 'w', newline='') as writefile:
            writer = csv.writer(writefile) 
            for country in countries:
                writer.writerow(country.values())

        writefile.close() 

    readfile.close()


def get_country_objects(filename: str):
    from models import engine, db_session, Country 
    with open(filename, 'r') as readfile:
        reader = csv.reader(readfile) 
        country_list = []
        for index, row in enumerate(reader):
            print(f'row: {row}')
            if index == 0:
                continue
            if row[2] == '':
                row[2] = '0.0'

            try:
                country = Country(
                    name = row[0], 
                    total_cases = int(float(row[1])),
                    total_deaths = int(float(row[2])) 
                )
                country_list.append(country)

            except ValueError:
                country = Country(
                    name = row[0], 
                    total_cases = 0.0,
                    total_deaths = int(row[2]) 
                )
                country_list.append(country)

        return country_list


def get_day_data_objects(filename):
    from models import engine, db_session, DayData, Country
    with open(filename, 'r') as readfile:
        reader = csv.reader(readfile) 
        day_data_list = []
        for index, row in enumerate(reader):
            if index == 0:
                continue
            print(f'row: {row}')
            if index < 5:
                continue
            print(f'row[0]: {row[0]}')
            country = db_session.query(Country).filter_by(name = row[0]).first()
            date_data = [int(date_component) for date_component in row[1].split('-')]

            try:
                country_date = DayData(
                    country = country,
                    date = datetime.date(date_data[0], date_data[1], date_data[2]),
                    new_cases = int(row[2]),
                    new_deaths = int(float(row[3])),
                )
                print(f'country: {country_date.new_cases}')
                day_data_list.append(country_date)

            except ValueError:
                country_date = DayData(
                    country = country,
                    date = datetime.date(date_data[0], date_data[1], date_data[2]),
                    new_cases = int(row[2]),
                    new_deaths = 0
                )
                day_data_list.append(country_date)
        
        return day_data_list


# class Loader:
#     def __init__(self):
#         from models import db_session 
#         self.session = db_session
#         self.country_loader = self.CountryLoader()
#         self.day_data_loader = self.DayDataLoader() 
    
#     class CountryLoader(DataLoader):
#         def batch_load_fn(self, keys, filename):
#             from models import db_session
#             country_data = get_country_objects(filename)
#             return Promise.resolve([self.session.add(country) for country in country_data])

#     class DayDataLoader(DataLoader):
#         def batch_load_fn(self, keys, filename):
#             day_data = get_day_data_objects(filename) 
#             return Promise.resolve([self.session.add(day) for day in day_data])

#     def finalize(self):
#         self.session.commit()


def record_updates():
    from models import db_session, DatabaseUpdate
    update = DatabaseUpdate(
        date = datetime.datetime.now()
    ) 
    db_session.add(update) 
    db_session.commit()



# -------------------------------------------- 

def fetch_and_display_headers():
    from pprint import pprint
    headers = []
    for f in os.listdir('CSSEGISandData'):
        with open(f'CSSEGISandData/{f}', 'r') as readfile:
            reader = csv.reader(readfile) 
            for i, row in enumerate(reader):
                if i > 0: break
                if len(headers) > 0:
                    if row == headers[-1]:
                        break
                headers.append(row) 
        readfile.close()
    pprint(headers)


def test_header_locator():
    from pprint import pprint
    list_of_file_item_samples = []
    relevent_header_index_set = 0

    for f in os.listdir('CSSEGISandData'):
        with open(f'CSSEGISandData/{f}', 'r') as readfile:
            reader = csv.reader(readfile) 
            for i, row in enumerate(reader):
                if i > 1: break
                if i == 0:
                    for key in file_headers.keys():
                        if row == file_headers[key]['headers']:
                            relevent_header_index_set = key
                            continue
                
                # print(row, file_headers[relevent_header_index_set]['index_array'].values())
                try:
                    values = [row[i] for i in file_headers[relevent_header_index_set]['index_array'].values()] 
                except IndexError:
                    break
                list_of_file_item_samples.append(values) 
        readfile.close()
    pprint(list_of_file_item_samples)


def sort_rows_by_country(filename, relevent_header_index):
    rows = []
    with open(filename, 'r') as readfile:
        reader = csv.reader(readfile) 
        # print(f'reader 0: {[row for row in reader][3]}')
        rows = sorted([row for row in reader], key = lambda x: (x[file_headers[relevent_header_index]['index_array']['country']], x[file_headers[relevent_header_index]['index_array']['province']]) )
        print(f'rows: {rows}')
    readfile.close()  
    return rows

# def reformat_dates(filename):
#     with open(filename, 'w') as writefile:
#         writer

def parse_and_compile_files():
    writeable_content = []
    relevent_header_index = 0
    for f in os.listdir('CSSEGISandData'):
        with open(f'CSSEGISandData/{f}', 'r') as readfile:
            reader = csv.reader(readfile)
            for i, row in enumerate(reader):
                if i == 0: 
                    for key in file_headers.keys():
                        if file_headers[key]['headers'] == row:
                            relevent_header_index = key 
                            break 
                    continue 
                try:
                    values = [row[i] for i in file_headers[relevent_header_index]['index_array'].values()]
                except:
                    pass
                writeable_content.append(row) 
        readfile.close()

    # reformat faulty formatted dates
    import re
    date_reformatter = lambda x: x.insert( 4, datetime.datetime.strptime(x[4].split(' ')[0], '%m/%d/%y').strftime('%m-%d-%Y') ) if re.search("/", x[4].split(' ')[0]) is not None else x
    writeable_content = map(date_reformatter, writeable_content)
    print(f'writebale_content: {writeable_content}')
    with open('CSSEGISandData/FinalData.csv', 'w', newline = '') as writefile:
        writer = csv.writer(writefile) 
        for row in writeable_content:
            print(f'row in writable content: {row}')
            try:
                writer.writerow(row) 
            except:
                pass
    writefile.close() 

    sorted_final_data = sort_rows_by_country('CSSEGISandData/FinalData.csv', relevent_header_index) 
    print(f'sorted files: {sorted_final_data}')
    # open('CSSEGISandData/FinalData.csv', 'w').close()
    with open('CSSEGISandData/FinalData.csv', 'w', newline = '') as writefile:
        writer = csv.writer(writefile) 
        for row in sorted_final_data:
            writer.writerow(row) 
    writefile.close()


def update_from_latest_file():
    import re
    from models import db_session, Country, DayData
    files = os.listdir('current_date_data') 
    # last_country = session.query(Country).order_by(Country.id.desc()).first() 
    # last_country_total_cases = last_country.total_cases
    # last_country_total_deaths = last_country.total_deaths
    with open(f'current_date_data/{files[0]}', 'r') as readfile:
        reader = csv.reader(readfile) 
        for i, row in enumerate(reader):
            if i == 0: continue
            if row[file_headers[6]['index_array']['country']] == 'US': continue
            if row[file_headers[6]['index_array']['province']] != '': continue 

            row[file_headers[6]['index_array']['country']] = '_'.join(row[file_headers[6]['index_array']['country']].split(' '))

            

            print(f'i: {i}')
            print('name: {}'.format(row[file_headers[6]['index_array']['country']]))
            # print('country_name: {}'.format(row[file_headers[6]['index_array']['country']]))
            try:
                relevent_country = db_session.query(Country).filter_by(name = row[file_headers[6]['index_array']['country']]).first()
            except:
                if len(relevent_country.name.split(' ')) > 1:
                    for i, country_name_part in enumerate(relevent_country.name.split(' ')):
                        try:
                            relevent_country = db_session.query(Country).filter_by(name = row[file_headers[6]['index_array']['country']].split(' ')[i]).first()
                            if relevent_country != None:
                                break
                        except:
                            pass
            if relevent_country is None: continue
            # print(f'country_object: {dir(relevent_country)}')
            last_country_total_cases = relevent_country.total_cases
            last_country_total_deaths = relevent_country.total_deaths
            print(f'last_country_total_cases: {last_country_total_cases}')
            date = row[file_headers[6]['index_array']['last_update']].split(' ')[0]
            # date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('')
            # print(f'list index out of range: {date_components}')

            date_reformatter = lambda x: x.insert( 4, datetime.datetime.strptime(x[4].split(' ')[0], '%m/%d/%y').strftime('%m-%d-%Y') ) if re.search("/", x[4].split(' ')[0]) is not None else x
            # writeable_content = map(date_reformatter, writeable_content)

            from sqlalchemy import update
            # country = Country(
            #     name = row[file_headers[6]['index_array']['country']],
            #     total_cases = int(last_country_total_cases) + int(row[file_headers[6]['index_array']['confirmed']]),
            #     total_deaths = int(last_country_total_deaths) + int(row[file_headers[6]['index_array']['deaths']])
            # )
            update(Country).where(Country.name == relevent_country.name).\
                values(
                    name = row[file_headers[6]['index_array']['country']],
                    total_cases = int(last_country_total_cases) + int(row[file_headers[6]['index_array']['confirmed']]),
                    total_deaths = int(last_country_total_deaths) + int(row[file_headers[6]['index_array']['deaths']])
                )

            day_data = DayData(
                country = relevent_country,
                date = datetime.date(int(date.split('-')[0]), int(date.split('-')[1]), int(date.split('-')[2])),
                new_cases = int(row[file_headers[6]['index_array']['confirmed']]),
                new_deaths = int(row[file_headers[6]['index_array']['deaths']])
            )
            print(f'country: {relevent_country} \nday_data: {day_data}')
            db_session.add(relevent_country) 
            db_session.add(day_data) 
            db_session.commit()
    readfile.close()


def alternatePullDownData(fetch_one = True):
    def fetch_it(days: int, allow_fetching_error = False, allow_fetching_error_count: int = 2):
        import re 

        current_date: datetime.date = ''

        if not allow_fetching_error:
            current_date = date.today() - timedelta(days = days)
            current_date = f'{current_date}'.split('-') 
            current_date = '-'.join([current_date[1], current_date[2], current_date[0]])

            request_url = f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{current_date}.csv' 
            r = requests.get(request_url, allow_redirects = True) 
            # print(f'r.content: {r.content}')
            byte_regex = re.compile(b'404')
            if r.content == b'404: Not Found':
                print(f'not found!!!!!!!!!!! \nCurrent date: {current_date}')
                return ValueError
            
            # print(f'made it here: {r.content}')
            open(f'current_date_data/{current_date}.csv', 'wb').write(r.content) 
            return
        else:
            current_date = date.today() - timedelta(days = days + allow_fetching_error_count)
            # print(f'current date: {str(current_date)}')
            current_date = f'{current_date}'.split('-') 
            current_date = '-'.join([current_date[1], current_date[2], current_date[0]])

        request_url = f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{current_date}.csv' 
        r = requests.get(request_url, allow_redirects = True) 
        print(f'r.content: {r.content}')
        if re.search("404", str(r.content)):
            if allow_fetching_error_count == 0:
                return ValueError
            else:
                print(f'r.content: {r.content}')
                allow_fetching_error_count -= 1 
                fetch_it(days = days, allow_fetching_error_count=allow_fetching_error_count)
        print(f'made it here: {r.content}')
        open(f'CSSEGISandData/{current_date}.csv', 'wb').write(r.content) 

    if not fetch_one:
        fetching = True 
        days = 0
        while fetching:
            try:
                print('fetching_it')
                fetch_it(days)
                days += 1
            except Exception as e:
                print(f'failed for some reason: {e}')
                fetching = False 
    else:
        # from models import session, DatabaseUpdate
        # update = session.query(DatabaseUpdate).order_by(ObjectRes.id.desc()).first()  
        # days = update.date - timedelta()
        try:
            fetch_it(1)
        except ValueError:
            fetch_it(1)
        return

    writeable_content = []
    for f in os.listdir('CSSEGISandData'):
        with open(f'CSSEGISandData/{f}', 'r') as readfile:
            reader = csv.reader(readfile)
            for row in reader:
                writeable_content.append(row) 
        readfile.close()
    
    with open('CSSEGISandData/FinalData.csv', 'w', newline = '') as writefile:
        writer = csv.writer(writefile) 
        for row in writeable_content:
            writer.writerow(row) 
    writefile.close() 

    sorted_final_data = sort_rows_by_country('CSSEGISandData/FinalData.csv') 

    open('CSSEGISandData/FinalData.csv', 'w').close()
    with open('CSSEGISandData/FinalData.csv', 'w', newline = '') as writefile:
        writer = csv.writer(writefile) 
        for row in sorted_final_data:
            writer.writerow(row) 
    writefile.close() 


# --------------------------------------------


def update_one():
    alternatePullDownData() 
    print('PULLED DATA')
    update_from_latest_file()


def main():
    pullDownData()
    delete_all_from_tables() 
    convert_to_csv('covid.xls')
    alter_data('covid.csv')
    alter_day_data('covid.csv')
    write_csv_data_to_database('altered_covid.csv') 
    write_day_csv_data_to_database('day_data.csv')
    record_updates() 


if __name__ == '__main__':
    # from models import Country, DayData
    # from utils import BulkManager
    pullDownData()
    delete_all_from_tables() 
    convert_to_csv('covid.xls')
    alter_data('covid.csv')
    alter_day_data('covid.csv')
    write_csv_data_to_database('altered_covid.csv') 
    write_day_csv_data_to_database('day_data.csv')
    record_updates() 
    # countryManager = BulkManager(CountryModel) 
    # DayaDataManager = BulkManager(DayDataModel)

    # country_objects = get_country_objects('altered.csv') 
    # countryManager.

    # day_data_objects = get_day_data_objects('day_data.csv')

    