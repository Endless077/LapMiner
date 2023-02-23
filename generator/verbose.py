#  _______    ________ _______    ___  _______  _________  
# |_   __ \  |_   __  |_   __ \ .'   `|_   __ \|  _   _  | 
#   | |__) |   | |_ \_| | |__) /  .-.  \| |__) |_/ | | \_| 
#   |  __ /    |  _| _  |  ___/| |   | ||  __ /    | |     
#  _| |  \ \_ _| |__/ |_| |_   \  `-'  _| |  \ \_ _| |_    
# |____| |___|________|_____|   `.___.|____| |___|_____|

import re
import csv
import json
import io
import numpy as np
import pandas as pd
import database as db
import sqlite3
import utils

LAPS_HEADERS = {
    'lap_time': 'Lap_Time',
    'driver': 'Driver',
    'track_name': 'Track_Name',
    'vehicle_name': 'Vehicle_Name'
}

TRACK_HEADERS = {
    'track_name': 'Track_Name',
    'country': 'Country',
    'total_length': 'Length_(km)'
}

VEHICLE_HEADERS = {
    "vehicle_name": "Vehicle_Name",
    "type": "Type",
    "manufacturer": "Manufacturer",
    "model": "Model",
    "origin_country": "Country",
    "introduced_year": "Introduced_Year",
    "accelleration": "0-100_kph_(s)",
    "break_distance": "100-0_(m)",
    "top_speed": "Top_Speed_(kph)",
    "curb_weight": "Curb_Weight_(kg)",
    "wheelbase": "Wheelbase_(m)",
    "length": "Length_(m)",
    "width": "Width_(m)",
    "height": "Height_(m)",
    "engine_name": "Engine",
    "displacement": "Displacement_(l)",
    "power": "Power_(ps)",
    "torque": "Torque_(Nm)",
    "engine_layout": "Engine_Layout",
    "wheel_drive": "Wheel_Drive",
    "class_type": "Class",
    "trasmission_name": "Trasmission_Name",
    "trasmission_type": "Trasmission_Type",
    "n_trasmission": "N_Trasmission"
}

PATH = "../LapMiner/report"

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

    conn = utils.get_SQLite_connection(db.PATH)
    db.create_views(conn, min_track_laps, min_vehicle_laps)
    return conn
     
def dataset_generator(conn: sqlite3.Connection):
    # Get all datasets and convert in varius format
    # :param conn: a connection to scrap.db (with TEMP views).
    # :return:

    laps_dataframe = pd.read_sql_query('SELECT * FROM EXPORT_LAP_LIST', conn)
    tracks_dataframe = pd.read_sql_query('SELECT * FROM EXPORT_TRACK_LIST', conn)
    vehicles_dataframe = pd.read_sql_query('SELECT * FROM EXPORT_VEHICLE_LIST', conn)

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

###########################################

def export_excel(datasets: dict):
    # Generate a excel file with all dataset in sheets
    # :param datasets: a dictionary with all dataframes.
    # :return:

    excel_path = PATH + '/excel/'

    print("Generating excel dataset...")
    with pd.ExcelWriter(excel_path + 'dataset.xlsx') as writer:
        for key,value in datasets.items():
            value.to_excel(writer, sheet_name=key, index=False)

def export_csv(datasets: dict):
    # Generate a csv file for each dataset
    # :param datasets: a dictionary with all dataframes.
    # :return:

    csv_path = PATH + '/csv/'
    
    print("Generating csv dataset...")
    for key,value in datasets.items():
        value.to_csv(f'{csv_path}{key}.csv', index=False)

def export_json(datasets: dict):
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

    with open(f"{json_path}vehicles.json", "w") as outfile:
        outfile.write(json_object_vehicles)

def json_track(laps_df: pd.DataFrame, tracks_df: pd.DataFrame):
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

def json_vehicle(laps_df: pd.DataFrame, vehicles_df: pd.DataFrame):
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

###########################################

def report():
    # Get a simple report of all data in the scrap dataset
    # :param:
    # :return: a report.txt file.
    
    print("Getting datasets...")
    with open(f'{PATH}/json/vehicles.json') as f1:
        json_vehicles = json.load(f1)
    with open(f'{PATH}/json/tracks.json') as f2:
        json_tracks = json.load(f2)
    
    df_laps = pd.read_csv(f'{PATH}/csv/Laps_Dataset.csv')
    df_tracks = pd.read_csv(f'{PATH}/csv/Tracks_Dataset.csv')
    df_vehicles = pd.read_csv(f'{PATH}/csv/Vehicle_Dataset.csv')

    report_file_laps = open(f'{PATH}/report_laps.txt', 'w')
    report_file_tracks = open(f'{PATH}/report_tracks.txt', 'w')
    report_file_vehicles = open(f'{PATH}/report_vehicles.txt', 'w')

    print("Starting laps stats...")
    report_laps(report_file_laps, df_laps.copy(), df_tracks.copy(), df_vehicles.copy(), json_tracks, json_vehicles)
    print("Starting tracks stats...")
    report_tracks(report_file_tracks, df_tracks.copy(), json_tracks)
    print("Starting vehicles stats...")
    report_vehicles(report_file_vehicles, df_vehicles.copy(), json_vehicles)
    print("Report complete.")

def matrix_generator(tracks: list):
    # Generate a comlete matrix Vehicles X Tracks whit (best) laptime
    # :param: (insert a list of tracks name in tracks variable - row 258)
    # :return: a matrix.txt file (and other format).

    matrix_path = PATH + '/matrix/'

    print("Getting datasets...")
    # with open(f'{PATH}/json/vehicles.json') as f1:
    #     json_vehicle = json.load(f1)
    with open(f'{PATH}/json/tracks.json') as f2:
        json_track = json.load(f2)
    
    # df_laps = pd.read_csv(f'{PATH}/csv/Laps_Dataset.csv')
    # df_tracks = pd.read_csv(f'{PATH}/csv/Tracks_Dataset.csv')
    # df_vehicles = pd.read_csv(f'{PATH}/csv/Vehicle_Dataset.csv')

    print("Starting matrix generation...")
    tracks_occ = [track for track in tracks if track in json_track.keys()]
    for track in tracks_occ:
        print(f"-Found {track} track.")

    # Classic approch
    vehicles_occ = {}

    count_occ = open(f'{PATH}/matrix/occurrences.txt', 'w')
    count_occ.write("occurrences.txt\n\n")

    for track in tracks_occ:
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
    dataframe = pd.DataFrame(columns=tracks_occ)

    matrix = open(f'{PATH}/matrix/matrix.txt', 'w')
    matrix.write("matrix.txt\n\n")

    for track in tracks_occ:
        for vehicle,laptimes in json_track[track]["Laps"].items():
            if(vehicle not in dataframe.index):
                dataframe.loc[vehicle] = pd.Series(None, dtype="float64", index=dataframe.columns)
            dataframe.loc[vehicle][track] = laptimes[0]

    dataframe.to_csv(f'{matrix_path}/matrix.csv')
    matrix.write(dataframe.to_markdown())

    print("Matrix complete.")

def report_laps(file: io.TextIOWrapper, laps: pd.DataFrame, tracks: pd.DataFrame, vehicles: pd.DataFrame, json_tracks: dict, json_vehicles: dict):
    # Write in report.txt a list of varius laps stats
    # :param file: linked file object ov report.txt
    # :param laps: laps dataframe copy.
    # :param tracks: tracks dataframe copy.
    # :param vehicles: vehicles dataframe copy.
    # :param json_tracks: the tracks json file.
    # :param json_vehicles: the vehicles json file.
    # :return:

    #report_laps_plot()

    # Mode no built-in function
    def mode(x):
        mode = x.mode()
        if mode.empty:
            return None
        else:
            return mode.iloc[0]
        
    file.write("report_laps.txt\n\n")

    file.write("####################################################################################################################################\n\n")

    file.write("-Laps report:\n")
    file.write(f"--Laps count: {laps.shape[0]}\n\n")

    file.write("######################\n\n")

    file.write("--Tracks laptimes stats:\n\n")
    df = tracks.join(laps.set_index('Track_Name'), on="Track_Name").groupby('Track_Name')
    df = df['Lap_Time'].agg(Lap_Counter='count',Lap_Mean='mean',Lap_Mode=mode,Lap_Median='median',Lap_Max='max',Lap_Min='min').sort_values(['Lap_Counter'], ascending=False)
    file.write(df.to_markdown() + '\n\n')
    
    file.write("######################\n\n")

    file.write("--Tracks best and worse vehicles:\n\n")
    df = tracks.join(laps.set_index('Track_Name'), on="Track_Name").set_index('Vehicle_Name').groupby('Track_Name')
    df = df['Lap_Time'].agg(WorseTime='idxmax', BestTime='idxmin')[['WorseTime','BestTime']]
    file.write(df.to_markdown() + '\n\n')

    file.write("######################\n\n")
    file.write("--Track vehicles stats:\n\n")
    df = laps.join(vehicles.set_index("Vehicle_Name"), on='Vehicle_Name').groupby(['Track_Name'])
    df = df['Power_(ps)'].agg(Power_Mean='mean',Power_Mode=mode,Power_Median='median',Power_Max='max',Power_Min='min')[['Power_Mean','Power_Mode','Power_Median','Power_Max','Power_Min']]
    file.write(df.to_markdown() + '\n\n')

    file.write("######################\n\n")
    file.write("--Track vehicles category count:\n\n")
    df = laps.join(vehicles.set_index("Vehicle_Name"), on='Vehicle_Name').groupby(['Track_Name','Type'])
    df = df['Lap_Time'].count()
    file.write(df.to_markdown() + '\n\n')

    file.write("######################\n\n")
    file.write("--Vehicle tracks stats:\n\n")
    df = laps.join(vehicles.set_index("Vehicle_Name"), on='Vehicle_Name').groupby(['Vehicle_Name','Track_Name'])
    df = df['Lap_Time'].agg(['count','mean',mode,'median','max','min']).sort_values(['count'], ascending=False)
    file.write(df.to_markdown() + '\n\n')

    file.write("######################\n\n")
    file.write("--Vehicle laps count:\n\n")
    df = laps.join(vehicles.set_index("Vehicle_Name"), on='Vehicle_Name').groupby(['Vehicle_Name'])
    df = df['Lap_Time'].agg(Laps='count')[['Laps']].sort_values('Laps', ascending=False)
    file.write(df.to_markdown() + '\n\n')

    file.write("####################################################################################################################################\n\n")
    file.close()

def report_laps_plot():
    raise NotImplementedError

def report_tracks(file: io.TextIOWrapper, tracks: pd.DataFrame, json_tracks: dict):
    # Write in report.txt a list of varius tracks stats
    # :param file: linked file object ov report.txt
    # :param tracks: tracks dataframe copy.
    # :param json_tracks: the tracks json file.
    # :return:
    
    #report_tracks_plot()

    # Mode no built-in function
    def mode(x):
        mode = x.mode()
        if mode.empty:
            return None
        else:
            return mode.iloc[0]
    
    file.write("report_tracks.txt\n\n")

    file.write("####################################################################################################################################\n\n")

    file.write("-Tracks report:\n")
    file.write(f"--Tracks count: {tracks.shape[0]}\n\n")

    file.write("######################\n\n")

    file.write("--Tracks country stats:\n\n")
    df = tracks.groupby('Country')
    df = df['Length_(km)'].agg(Length_Counter='count',Length_Mean='mean',Length_Mode=mode,Lengt_Median='median',Length_Max='max',Length_Min='min').sort_values(['Length_Counter'], ascending=False)
    file.write(df.to_markdown() + '\n\n')

    file.write("######################\n\n")

    file.write("--Tracks length stats:\n\n")
    df = tracks.set_index('Track_Name').groupby('Country')
    df = df['Length_(km)'].agg(Length_Max='idxmax', Length_Min='idxmin')[['Length_Max','Length_Min']]
    file.write(df.to_markdown() + '\n\n')

    file.write("####################################################################################################################################\n\n")
    file.close()

def report_tracks_plot():
    raise NotImplementedError

def report_vehicles(file: io.TextIOWrapper, vehicles: pd.DataFrame, json_vehicles: dict):
    # Write in report.txt a list of varius vehicles stats
    # :param file: linked file object ov report.txt
    # :param vehicles: vehicles dataframe copy.
    # :param json_vehicles: the vehicles json file.
    # :return:

    #report_vehicles_plot()

    # Mode no built-in function
    def mode(x):
        mode = x.mode()
        if mode.empty:
            return None
        else:
            return mode.iloc[0]
    
    file.write("report_vehicles.txt\n\n")

    file.write("####################################################################################################################################\n\n")

    file.write("-Vehicle report:\n")
    file.write(f"--Vehicle_count: {vehicles.shape[0]}\n\n")

    file.write("######################\n\n")
    
    file.write("--Vehicles type count:\n\n")
    df = vehicles.groupby("Class")['Vehicle_Name'].agg(Vehicle='count')[['Vehicle']].sort_values(['Vehicle'], ascending=False)
    file.write(df.to_markdown() + '\n\n')

    file.write("######################\n\n")

    file.write("--Vehicles country count (origin Country):\n\n")
    df = vehicles.groupby(["Country","Type"])['Vehicle_Name'].agg(Vehicle='count')[['Vehicle']].sort_values(['Vehicle'], ascending=False)
    file.write(df.to_markdown() + '\n\n')

    file.write("######################\n\n")

    file.write("--Vehicles class dimensions:\n\n")
    df = vehicles.groupby('Class')[["Curb_Weight_(kg)","Wheelbase_(m)","Length_(m)","Width_(m)","Height_(m)"]].agg(['mean',mode,'median','max','min'])
    file.write(df.to_markdown() + '\n\n')

    file.write("######################\n\n")

    file.write("--Vehicles class performance:\n\n")
    df = vehicles.groupby('Class')[["Top_Speed_(kph)","0-100_kph_(s)","Power_(ps)","Torque_(Nm)"]].agg(['mean',mode,'median','max','min'])
    file.write(df.to_markdown() + '\n\n')

    file.write("######################\n\n")

    file.write("--Vehicles manufacturer dimensions:\n\n")
    df = vehicles.groupby('Manufacturer')[["Curb_Weight_(kg)","Wheelbase_(m)","Length_(m)","Width_(m)","Height_(m)"]].agg(['mean',mode,'median','max','min'])
    file.write(df.to_markdown() + '\n\n')

    file.write("######################\n\n")

    file.write("--Vehicles manufacturer performance:\n\n")
    df = vehicles.groupby('Manufacturer')[["Top_Speed_(kph)","0-100_kph_(s)","Power_(ps)","Torque_(Nm)"]].agg(['mean',mode,'median','max','min'])
    file.write(df.to_markdown() + '\n\n')

    file.write("######################\n\n")
    
    file.write("--Vehicles country dimensions:\n\n")
    df = vehicles.groupby('Country')[["Curb_Weight_(kg)","Wheelbase_(m)","Length_(m)","Width_(m)","Height_(m)"]].agg(['mean',mode,'median','max','min'])
    file.write(df.to_markdown() + '\n\n')

    file.write("######################\n\n")

    file.write("--Vehicles country performance:\n\n")
    df = vehicles.groupby('Country')[["Top_Speed_(kph)","0-100_kph_(s)","Power_(ps)","Torque_(Nm)"]].agg(['mean',mode,'median','max','min'])
    file.write(df.to_markdown() + '\n\n')

    file.write("####################################################################################################################################\n\n")
    file.close()

def report_vehicles_plot():
    raise NotImplementedError
