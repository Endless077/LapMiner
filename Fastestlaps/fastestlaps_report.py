# Fastestlaps report

import re
import csv
import json
import numpy as np
import pandas as pd
import fastestlaps_db as db

from IPython.display import display

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
    'Introduced_Year': 'Introduced Year',
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
        min_vehicle_laps = input("Insert min number of laptime per vehicle: ")
        min_track_laps = input("Insert min number of laptime per track: ")
        try:
            int(min_vehicle_laps)
            int(min_track_laps)
        except ValueError:
            print("Error input, insert valid value.")
        else:
            break
    
    conn = db.get_connection()
    db.filter(conn, min_track_laps, min_vehicle_laps)
    return conn
        
def dataset_generator(conn):
    
    laps_dataframe = pd.read_sql_query('SELECT * FROM Extract_Laps_List', conn)
    tracks_dataframe = pd.read_sql_query('SELECT * FROM Extract_Track_List', conn)
    vehicles_dataframe = pd.read_sql_query('SELECT * FROM Extract_Vehicle_List', conn)

    laps_dataframe.rename(columns=LAPS_HEADERS, inplace=True)
    tracks_dataframe.rename(columns=TRACK_HEADERS, inplace=True)
    vehicles_dataframe.rename(columns=VEHICLE_HEADERS, inplace=True)

    print("######################")
    display(laps_dataframe)
    print("######################")
    display(tracks_dataframe)
    print("######################")
    display(vehicles_dataframe)
    print("######################")
    
    datasets = {
    'Laps_Dataset': laps_dataframe,
    'Tracks_Dataset': tracks_dataframe,
    'Vehicle_Dataset': vehicles_dataframe
    }

    export_excel(datasets)
    export_csv(datasets)
    export_json(datasets)

    print("Dataset exported in excel, csv and json format.")

def export_excel(datasets):
    excel_path = PATH + '/excel/'

    print("Generating excel dataset...")
    with pd.ExcelWriter(excel_path + 'dataset.xlsx') as writer:
        for key,value in datasets.items():
            value.to_excel(writer, sheet_name=key, index=False)

def export_csv(datasets):
    csv_path = PATH + '/csv/'
    
    print("Generating csv dataset...")
    for key,value in datasets.items():
        value.to_csv(f'{csv_path}{key}.csv', index=False)

def export_json(datasets):
    json_path = PATH + '/json/'

    laps_df = datasets['Laps_Dataset']
    tracks_df = datasets['Tracks_Dataset']
    vehicles_df = datasets['Vehicle_Dataset']

    print("Generating json dataset...")
    tracks = json_track(laps_df.copy(), tracks_df.copy())
    vehicles = json_vehicle(laps_df.copy(), vehicles_df.copy())

    json_object_tracks = json.dumps(tracks, ensure_ascii=False, indent = 3)
    json_object_vehicles = json.dumps(vehicles, ensure_ascii=False, indent = 3)

    with open(f"{json_path}tracks.json", "w") as outfile:
        outfile.write(json_object_tracks)

    with open(f"{json_path}vehicle.json", "w") as outfile:
        outfile.write(json_object_vehicles)

def json_track(laps_df, tracks_df):
    tracks_json = {}

    for track_row in tracks_df.itertuples(name=None):
        tracks_json[track_row[1]] = {}

        tracks_json[track_row[1]]["Laps"] = {}
        tracks_json[track_row[1]]["Country"] = track_row[2]
        tracks_json[track_row[1]]["Track Length"] = track_row[3]

        curr_track = laps_df.loc[(laps_df["Track Name"] == track_row[1]), ["Vehicle Name", "Lap Time"]].sort_values(by="Lap Time")

        for lap_row in curr_track.itertuples(name=None):
            if(lap_row[1] in tracks_json[track_row[1]]["Laps"].keys()):
                tracks_json[track_row[1]]["Laps"][lap_row[1]].append(lap_row[2])
            else:
             tracks_json[track_row[1]]["Laps"][lap_row[1]] = [lap_row[2]]
    
    return tracks_json

def json_vehicle(laps_df, vehicles_df):
    vehicle_json = {}

    for vehicle_row in vehicles_df.itertuples(name=None):
        vehicle_json[vehicle_row[1]] = {}
        vehicle_json[vehicle_row[1]]["Laps"] = {}
        vehicle_json[vehicle_row[1]]["Specs"] = {}
        attr = 1

        for key,value in VEHICLE_HEADERS.items():
            vehicle_json[vehicle_row[1]]["Specs"][value] = vehicle_row[attr]
            attr += 1

        curr_vehicle = laps_df.loc[(laps_df["Vehicle Name"] == vehicle_row[1]), ["Track Name", "Lap Time"]].sort_values(by="Lap Time")
        
        for lap_row in curr_vehicle.itertuples(name=None):
            if(lap_row[1] in vehicle_json[vehicle_row[1]]["Laps"].keys()):
                vehicle_json[vehicle_row[1]]["Laps"][lap_row[1]].append(lap_row[2])
            else:
             vehicle_json[vehicle_row[1]]["Laps"][lap_row[1]] = [lap_row[2]]

    return vehicle_json

def report():
    raise NotImplementedError
