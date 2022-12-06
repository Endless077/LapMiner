# Fastestlaps report

import re
import csv
import json
import numpy as np
import pandas as pd
import fastestlaps_db as db

LAPS_HEADERS = {
    'Lap_Time': 'Lap Time',
    'Driver': 'Driver',
    'PS_KG': 'PS/KG',
    'Track': 'Track Name',
    'Vehicle': 'Vehicle Name'
}
TRACK_HEADERS = {
    'Track_Name': 'Track Name',
    'Country': 'Country',
    'Total_Lenght': 'Length (km)'
}
VEHICLE_HEADERS = {
	'Vehicle': 'Vehicle Name',
	'Type': 'Type',
	'Type_Usage': 'Type Usage',
    'Introduced_Year': 'Introduced_Year',
    'Country': 'Country',
	'Curb_Weight': 'Curb Weight (kg)',
	'Wheelbase': 'Wheelbase (m)',
	'Dim_Long': 'Long (m)',
	'Dim_Wide': 'Wide (m)',
	'Dim_High': 'High (m)',
	'Zero_Hundred': '0-100 kph (s)',
	'Hundred_Zero': '100-0 kph (s)',
	'Top_Speed': 'Top Speed (s)',
	'Engine_Type': 'Engine',
	'Displacement': 'Displacement (l)',
	'Power_PS': 'Power (ps)',
	'Power_BHP': 'Power (bhp)',
	'Power_KW': 'Power (kw)',
	'Torque': 'Torque (Nm)',
	'Power_Weight': 'Power/Weight (ps)' ,
	'Torque_Weight': 'Torque/Weight (Nm)',
	'Efficiency': 'Efficiency (ps per l/100 km)',
	'Trasmissions': 'Trasmission',
	'Layout': 'Layout',
}

PATH = "./report"

def extract_dataset():
    print("Extracting dataset...")
    while True:
        min_vehicle_laps = input("Inserire numero minimo di laptime per veicolo: ")
        min_track_laps = input("Inserire numero minimo di laptime per circuito: ")
        try:
            int(min_vehicle_laps)
            int(min_track_laps)
        except ValueError:
            print("Errore di input, inserire valori validi.")
        else:
            break
    
    conn = db.get_connection()
    db.extract_database(conn, min_track_laps, min_vehicle_laps)
    return conn

def report_generator():
    raise NotImplementedError

def report_csv(conn):
    print("Generating excel and csv dataset...")
    excel_path = PATH + '/excel'
    csv_path = PATH + '/csv'
    
    laps_dataframe = pd.read_sql_query('SELECT * FROM Extract_Laps_List', conn)
    tracks_dataframe = pd.read_sql_query('SELECT * FROM Extract_Track_List', conn)
    vehicles_dataframe = pd.read_sql_query('SELECT * FROM Extract_Vheicle_List', conn)

    laps_dataframe.rename(columns=LAPS_HEADERS, inplace=True)
    tracks_dataframe.rename(columns=TRACK_HEADERS, inplace=True)
    vehicles_dataframe.rename(columns=VEHICLE_HEADERS, inplace=True)
    
    with pd.ExcelWriter(excel_path + 'dataset.xlsx') as writer:
        laps_dataframe.to_excel(writer, sheet_name="Laps_Time")
        tracks_dataframe.to_excel(writer, sheet_name="Tracks")
        vehicles_dataframe.to_excel(writer, sheet_name="Vehicles")

    laps_dataframe.to_csv(csv_path + 'laps_time.csv')
    tracks_dataframe.to_csv(csv_path + 'tracks.csv')
    vehicles_dataframe.to_csv(csv_path + 'vehicles.csv')

def report_json():
    raise NotImplementedError