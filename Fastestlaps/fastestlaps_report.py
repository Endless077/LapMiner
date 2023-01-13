#  _______    ________ _______    ___  _______  _________  
# |_   __ \  |_   __  |_   __ \ .'   `|_   __ \|  _   _  | 
#   | |__) |   | |_ \_| | |__) /  .-.  \| |__) |_/ | | \_| 
#   |  __ /    |  _| _  |  ___/| |   | ||  __ /    | |     
#  _| |  \ \_ _| |__/ |_| |_   \  `-'  _| |  \ \_ _| |_    
# |____| |___|________|_____|   `.___.|____| |___|_____|

import re
import csv
import json
import numpy as np
import pandas as pd
import fastestlaps_db as db

LAPS_HEADERS = {
    'Lap_Time': 'Lap_Time',
    'Driver': 'Driver',
    'PS_KG': 'PS/KG',
    'Track': 'Track_Name',
    'Vehicle': 'Vehicle_Name'
}
TRACK_HEADERS = {
    'Track_Name': 'Track_Name',
    'Country': 'Country',
    'Total_Length': 'Length_(km)'
}
VEHICLE_HEADERS = {
	'Vehicle': 'Vehicle_Name',
	'Type': 'Type',
	'Type_Usage': 'Type_Usage',
    'Introduced_Year': 'Introduced_Year',
    'Country': 'Country',
	'Curb_Weight': 'Curb_Weight_(kg)',
	'Wheelbase': 'Wheelbase_(m)',
	'Dim_Long': 'Long_(m)',
	'Dim_Wide': 'Wide_(m)',
	'Dim_High': 'High_(m)',
	'Zero_Hundred': '0-100_kph_(s)',
	'Hundred_Zero': '100-0_kph_(m)',
	'Top_Speed': 'Top_Speed_(s)',
	'Engine_Type': 'Engine',
	'Displacement': 'Displacement_(l)',
	'Power_PS': 'Power_(ps)',
	'Power_BHP': 'Power_(bhp)',
	'Power_KW': 'Power_(kw)',
	'Torque': 'Torque_(Nm)',
	'Power_Weight': 'Power/Weight_(ps)' ,
	'Torque_Weight': 'Torque/Weight_(Nm)',
	'Efficiency': 'Efficiency_(ps_per_l/100_km)',
	'Trasmissions': 'Trasmission',
	'Layout': 'Layout',
}

PATH = "./report"

def extract_dataset():
    # Create a set of TEMP view in scrap.db
    # :param:
    # :return conn: the current connection to scrap.db.

    print("Extracting dataset...")
    while True:
        min_vehicle_laps = input("Insert min number of laptime per vehicle:\n")
        print(f"Number or min laptime per vehicle: {min_vehicle_laps}")
        min_track_laps = input("Insert min number of unique laptime per track:\n")
        print(f"Number or min unique laptime per track: {min_track_laps}")
        try:
            int(min_vehicle_laps)
            int(min_track_laps)
        except ValueError:
            print("Error input, insert a valid value.")
        else:
            break
    
    conn = db.get_connection()
    db.filter(conn, min_track_laps, min_vehicle_laps)
    return conn
     
def dataset_generator(conn):
    # Get all datasets and convert in varius format
    # :param conn: a connection to scrap.db (with TEMP views).
    # :return:

    laps_dataframe = pd.read_sql_query('SELECT * FROM Extract_Laps_List', conn)
    tracks_dataframe = pd.read_sql_query('SELECT * FROM Extract_Track_List', conn)
    vehicles_dataframe = pd.read_sql_query('SELECT * FROM Extract_Vehicle_List', conn)

    laps_dataframe.rename(columns=LAPS_HEADERS, inplace=True)
    tracks_dataframe.rename(columns=TRACK_HEADERS, inplace=True)
    vehicles_dataframe.rename(columns=VEHICLE_HEADERS, inplace=True)

    print("######################")
    print(laps_dataframe)
    print("######################")
    print(tracks_dataframe)
    print("######################")
    print(vehicles_dataframe)
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
    # Generate a excel file with all dataset in sheets
    # :param datasets: a dictionary with all dataframes.
    # :return:

    excel_path = PATH + '/excel/'

    print("Generating excel dataset...")
    with pd.ExcelWriter(excel_path + 'dataset.xlsx') as writer:
        for key,value in datasets.items():
            value.to_excel(writer, sheet_name=key, index=False)

def export_csv(datasets):
    # Generate a csv file for each dataset
    # :param datasets: a dictionary with all dataframes.
    # :return:

    csv_path = PATH + '/csv/'
    
    print("Generating csv dataset...")
    for key,value in datasets.items():
        value.to_csv(f'{csv_path}{key}.csv', index=False)

def export_json(datasets):
    # Generate a json file for tracks and vehicle with some informations
    # :param datasets: a dictionary with all dataframes.
    # :return:

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
    # Generate a dict for a json converter (tracks)
    # :param laps_df: laps dataframe.
    # :param track_df: tracks dataframe.
    # :return: a dict for tracks

    tracks_json = {}

    for track_row in tracks_df.itertuples(name=None):
        tracks_json[track_row[1]] = {}

        tracks_json[track_row[1]]["Laps"] = {}
        tracks_json[track_row[1]]["Country"] = track_row[2]
        tracks_json[track_row[1]]["Track_Length"] = track_row[3]

        curr_track = laps_df.loc[(laps_df["Track_Name"] == track_row[1]), ["Vehicle_Name", "Lap_Time"]].sort_values(by="Lap_Time")

        for lap_row in curr_track.itertuples(name=None):
            if(lap_row[1] in tracks_json[track_row[1]]["Laps"].keys()):
                tracks_json[track_row[1]]["Laps"][lap_row[1]].append(lap_row[2])
            else:
             tracks_json[track_row[1]]["Laps"][lap_row[1]] = [lap_row[2]]
    
    return tracks_json

def json_vehicle(laps_df, vehicles_df):
     # Generate a dict for a json converter (vehicles)
    # :param laps_df: laps dataframe.
    # :param track_df: vehicles dataframe.
    # :return: a dict for vehicle

    vehicle_json = {}

    for vehicle_row in vehicles_df.itertuples(name=None):
        vehicle_json[vehicle_row[1]] = {}
        vehicle_json[vehicle_row[1]]["Laps"] = {}
        vehicle_json[vehicle_row[1]]["Specs"] = {}
        attr = 1

        for key,value in VEHICLE_HEADERS.items():
            vehicle_json[vehicle_row[1]]["Specs"][value] = vehicle_row[attr]
            attr += 1

        curr_vehicle = laps_df.loc[(laps_df["Vehicle_Name"] == vehicle_row[1]), ["Track_Name", "Lap_Time"]].sort_values(by="Lap_Time")
        
        for lap_row in curr_vehicle.itertuples(name=None):
            if(lap_row[1] in vehicle_json[vehicle_row[1]]["Laps"].keys()):
                vehicle_json[vehicle_row[1]]["Laps"][lap_row[1]].append(lap_row[2])
            else:
             vehicle_json[vehicle_row[1]]["Laps"][lap_row[1]] = [lap_row[2]]

    return vehicle_json

def report():
    # Get a simple report of all data in the scrap dataset
    # :param:
    # :return: a report.txt file.
    
    print("Getting datasets...")
    with open(f'{PATH}/json/vehicle.json') as f1:
        json_vehicle = json.load(f1)
    with open(f'{PATH}/json/tracks.json') as f2:
        json_track = json.load(f2)
    
    df_laps = pd.read_csv(f'{PATH}/csv/Laps_Dataset.csv')
    df_tracks = pd.read_csv(f'{PATH}/csv/Tracks_Dataset.csv')
    df_vehicles = pd.read_csv(f'{PATH}/csv/Vehicle_Dataset.csv')

    report = open(f'{PATH}/report.txt', 'w')
    report.write("report.txt\n\n")

    print("Starting laps stats...")
    report_laps(report, df_laps.copy(), df_tracks.copy(), df_vehicles.copy(), json_track, json_vehicle)
    print("Starting tracks stats...")
    report_tracks(report, df_tracks.copy(), json_track)
    print("Starting vehicles stats...")
    report_vehicles(report,df_vehicles.copy(), json_vehicle)
    print("Report complete.")

    report.write("####################################################################################################################################\n\n")
    report.close()

def matrix_generator():
    # Generate a comlete matrix Vehicles X Tracks whit (best) laptime
    # :param:
    # :return: a matrix.txt file (and other format).

    # Matrix generator
    print("Getting datasets...")
    with open(f'{PATH}/json/vehicle.json') as f1:
        json_vehicle = json.load(f1)
    with open(f'{PATH}/json/tracks.json') as f2:
        json_track = json.load(f2)
    
    df_laps = pd.read_csv(f'{PATH}/csv/Laps_Dataset.csv')
    df_tracks = pd.read_csv(f'{PATH}/csv/Tracks_Dataset.csv')
    df_vehicles = pd.read_csv(f'{PATH}/csv/Vehicle_Dataset.csv')

    print("Starting matrix generation...")
    tracks = []

    for track in tracks:
        print(f"-Found {track} track.")

    # Classic approch
    vehicles_occ = {}

    count_occ = open(f'{PATH}/matrix/occurrences.txt', 'w')
    count_occ.write("occurrences.txt\n\n")

    for track in tracks:
        for vehicle,laptimes in json_track[track]["Laps"].items():
            if(vehicle not in vehicles_occ.keys()):
                vehicles_occ[vehicle] = 1
            else:
                vehicles_occ[vehicle] += 1
    
    vehicles_occ_view = [ (times,vehicle) for vehicle,times in vehicles_occ.items() ]
    vehicles_occ_view.sort(reverse=True)
    for vehicle,times in vehicles_occ_view:
        count_occ.write("%s: %d\n" % (times,vehicle))


    # Pandas approch
    dataframe = pd.DataFrame(columns=tracks)

    matrix = open(f'{PATH}/matrix/matrix.txt', 'w')
    matrix.write("matrix.txt\n\n")

    for track in tracks:
        for vehicle,laptimes in json_track[track]["Laps"].items():
            if(vehicle not in dataframe.index):
                dataframe.loc[vehicle] = pd.Series(None, dtype="float64", index=dataframe.columns)
            dataframe.loc[vehicle][track] = laptimes[0]

    matrix.write(dataframe.to_markdown())
    print("Matrix complete.")

def report_laps(file, laps, tracks, vehicles, json_tracks, json_vehicles):
    # Write in report.txt a list of varius laps stats
    # :param file: linked file object ov report.txt
    # :param laps: laps dataframe copy.
    # :param tracks: tracks dataframe copy.
    # :param vehicles: vehicles dataframe copy.
    # :param json_tracks: the tracks json file.
    # :param json_vehicles: the vehicles json file.
    # :return:

    #report_laps_plot()

    file.write("####################################################################################################################################\n\n")
    file.write("-Laps report:\n")
    file.write(f"--Laps count: {laps.shape[0]}\n\n")

    file.write("######################\n\n")

    file.write("--Tracks laptimes stats:\n\n")
    df = tracks.join(laps.set_index('Track_Name'), on="Track_Name").groupby('Track_Name')
    df = df['Lap_Time'].agg(Lap_Counter='count',Lap_Mean='mean',Lap_Max='max',Lap_Min='min').sort_values(['Lap_Counter'], ascending=False)
    file.write(df.to_markdown() + '\n\n')
    
    file.write("######################\n\n")

    file.write("--Tracks best and worse vehicles:\n\n")
    df = tracks.join(laps.set_index('Track_Name'), on="Track_Name").set_index('Vehicle_Name').groupby('Track_Name')
    df = df['Lap_Time'].agg(WorseTime='idxmax', BestTime='idxmin')[['WorseTime','BestTime']]
    file.write(df.to_markdown() + '\n\n')

    file.write("######################\n\n")
    file.write("--Track vehicles stats:\n\n")
    df = laps.join(vehicles.set_index("Vehicle_Name"), on='Vehicle_Name').groupby(['Track_Name'])
    df = df['Power_(ps)'].agg(Power_Mean='mean',Power_Max='max',Power_Min='min')[['Power_Mean','Power_Max','Power_Min']]
    file.write(df.to_markdown() + '\n\n')

    file.write("######################\n\n")
    file.write("--Track vehicles category count:\n\n")
    df = laps.join(vehicles.set_index("Vehicle_Name"), on='Vehicle_Name').groupby(['Track_Name','Type_Usage'])
    df = df['Lap_Time'].count()
    file.write(df.to_markdown() + '\n\n')

    file.write("######################\n\n")
    file.write("--Vehicle tracks stats:\n\n")
    df = laps.join(vehicles.set_index("Vehicle_Name"), on='Vehicle_Name').groupby(['Vehicle_Name','Track_Name'])
    df = df['Lap_Time'].agg(['count','mean','max','min']).sort_values(['count'], ascending=False)
    file.write(df.to_markdown() + '\n\n')

    file.write("######################\n\n")
    file.write("--Vehicle laps count:\n\n")
    df = laps.join(vehicles.set_index("Vehicle_Name"), on='Vehicle_Name').groupby(['Vehicle_Name'])
    df = df['Lap_Time'].agg(Laps='count')[['Laps']].sort_values('Laps', ascending=False)
    file.write(df.to_markdown() + '\n\n')

def report_laps_plot():
    raise NotImplementedError

def report_tracks(file, tracks, json_tracks):
    # Write in report.txt a list of varius tracks stats
    # :param file: linked file object ov report.txt
    # :param tracks: tracks dataframe copy.
    # :param json_tracks: the tracks json file.
    # :return:
    
    #report_tracks_plot()

    file.write("####################################################################################################################################\n\n")
    file.write("-Tracks report:\n")
    file.write(f"--Tracks count: {tracks.shape[0]}\n\n")

    file.write("######################\n\n")

    file.write("--Tracks country stats:\n\n")
    df = tracks.groupby('Country')
    df = df['Length_(km)'].agg(Length_Counter='count',Length_Mean='mean',Length_Max='max',Length_Min='min').sort_values(['Length_Counter'], ascending=False)
    file.write(df.to_markdown() + '\n\n')

    file.write("######################\n\n")

    file.write("--Tracks length stats:\n\n")
    df = tracks.set_index('Track_Name').groupby('Country')
    df = df['Length_(km)'].agg(Length_Max='idxmax', Length_Min='idxmin')[['Length_Max','Length_Min']]
    file.write(df.to_markdown() + '\n\n')

def report_tracks_plot():
    raise NotImplementedError

def report_vehicles(file, vehicles, json_vehicles):
    # Write in report.txt a list of varius vehicles stats
    # :param file: linked file object ov report.txt
    # :param vehicles: vehicles dataframe copy.
    # :param json_vehicles: the vehicles json file.
    # :return:

    #report_vehicles_plot()

    file.write("####################################################################################################################################\n\n")
    file.write("-Vehicle report:\n")
    file.write(f"--Vehicle_count: {vehicles.shape[0]}\n\n")

    file.write("######################\n\n")
    
    file.write("--Vehicles type count (type Usage):\n\n")
    df = vehicles.groupby("Type_Usage")['Vehicle_Name'].agg(Vehicle='count')[['Vehicle']].sort_values(['Vehicle'], ascending=False)
    file.write(df.to_markdown() + '\n\n')

    file.write("######################\n\n")

    file.write("--Vehicles country count (origin Country):\n\n")
    df = vehicles.groupby(["Country","Type_Usage"])['Vehicle_Name'].agg(Vehicle='count')[['Vehicle']].sort_values(['Vehicle'], ascending=False)
    file.write(df.to_markdown() + '\n\n')

    file.write("######################\n\n")

    file.write("--Vehicles type dimensions:\n\n")
    df = vehicles.groupby('Type_Usage')[["Curb_Weight_(kg)","Wheelbase_(m)","Long_(m)","Wide_(m)","High_(m)"]].agg(['mean','max','min'])
    file.write(df.to_markdown() + '\n\n')

    file.write("######################\n\n")

    file.write("--Vehicles type performance:\n\n")
    df = vehicles.groupby('Type_Usage')[["Top_Speed_(s)","0-100_kph_(s)","Power_(ps)","Torque_(Nm)"]].agg(['mean','max','min'])
    file.write(df.to_markdown() + '\n\n')

    file.write("######################\n\n")

    file.write("--Vehicles country dimensions:\n\n")
    df = vehicles.groupby('Country')[["Curb_Weight_(kg)","Wheelbase_(m)","Long_(m)","Wide_(m)","High_(m)"]].agg(['mean','max','min'])
    file.write(df.to_markdown() + '\n\n')

    file.write("######################\n\n")

    file.write("--Vehicles country performance:\n\n")
    df = vehicles.groupby('Country')[["Top_Speed_(s)","0-100_kph_(s)","Power_(ps)","Torque_(Nm)"]].agg(['mean','max','min'])
    file.write(df.to_markdown() + '\n\n')

def report_vehicles_plot():
    raise NotImplementedError
