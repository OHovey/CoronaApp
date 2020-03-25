import pandas as pd
import csv
import datetime
from datetime import date
import requests
import sqlite3

def pullDownData():
    current_date = date.today()
    request_url = f'https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-2020-03-23.xlsx'

    r = requests.get(request_url, allow_redirects = True)
    open('covid.xls', 'wb').write(r.content)
# https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-2020-03-23.xlsx

def convert_to_csv(filename: str):
    excel_data = pd.read_excel(filename, 'COVID-19-geographic-disbtributi', index_col = None) 
    print(excel_data.head())
    excel_data.to_csv('covid.csv', encoding = 'utf-8')


def delete_all_from_tables():
    sql = 'DELETE FROM country' 
    sql2 = 'DELETE FROM country_history' 

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


if __name__ == '__main__':
    # from models import db_session
    pullDownData()
    delete_all_from_tables() 
    convert_to_csv('covid.xls')
    alter_data('covid.csv')
    alter_day_data('covid.csv')
    write_csv_data_to_database('altered_covid.csv') 
    write_day_csv_data_to_database('day_data.csv')
    