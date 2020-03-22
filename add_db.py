# import xlrd 
import pandas as pd
import csv
import datetime

def convert_to_csv(filename: str):
    excel_data = pd.read_excel(filename, 'CSV_4_COMS', index_col = None) 
    print(excel_data.head())
    excel_data.to_csv('covid_csv.csv', encoding = 'utf-8')


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
            print(f'row: {row}')
            if index < 5:
                continue
            # if row[2] == '':
            #     row[2] = '0.0'
            print(f'row[0]: {row[0]}')
            country = db_session.query(Country).filter_by(name = row[0]).first()
            # print(f'actual_id: {actual_id}')
            # print(f'country: {country_id.name}')
            # print(f'country: {db_session.query(Country).filter_by(id = country_id)}')
            date_data = [int(date_component) for date_component in row[1].split('-')]

            try:
                # if int(row[3]):
                #     row_three = int(row[3]) 
                # else:
                #     row_three = 0
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
                'country_name': row[2],
                'date': row[1].split(',')[0],
                'new_cases': int(row[3]),
                'new_deaths': row[4] 
            }
            data_points.append(day_data)
        
        with open('day_data.csv', 'w', newline='') as writefile:
            writer = csv.writer(writefile)
            for day in data_points:
                writer.writerow(day.values()) 
            
        writefile.close() 

    readfile.close() 

            # try:
                # day_data = DayData(
                #     country_name = row[2],
                #     date = row[1].split(',')[0],
                #     new_cases = int(row[3]),
                #     new_deaths = row[4] 
                # )
                # db_session.add(day_data)  

            # except ValueError:
            #     day_data = DayData(
            #         country_name = row[2], 
            #         date = row[1].split(',')[0],
            #         new_cases = int(row[3]),
            #         new_deaths = 0.0
            #     )
            #     db_session.

def alter_data(filename): 
    with open(filename, 'r') as readfile: 
        reader = csv.reader(readfile) 
        last_location = ''
        total_cases = 0 
        total_deaths = 0

        countries = []

        for index, row in enumerate(reader):
            if not index: continue
            if row[4] == '': row[4] = 0

            if row[2] == last_location:
                try:
                    total_cases += int(float(row[3])) 
                    total_deaths += int(float(row[4]))
                except ValueError:
                    total_cases += 0 
                    total_deaths += int(row[4]) 
            else:
                country_data = {
                    'name': last_location,
                    'total_cases': total_cases,
                    'total_deaths': total_deaths
                }
                countries.append(country_data) 

                last_location = row[2] 
                try:
                    total_cases += int(float(row[3])) 
                    total_deaths += int(float(row[4]))
                except ValueError:
                    total_cases += 0 
                    total_deaths += int(row[4]) 
                
                total_cases = 0 
                total_deaths = 0
        
        with open('altered_covid.csv', 'w', newline='') as writefile:
            writer = csv.writer(writefile) 
            for country in countries:
                writer.writerow(country.values())

        writefile.close() 

    readfile.close()
