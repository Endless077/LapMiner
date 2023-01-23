#  ______       _    _________    _      ______       _      ______  ________  
# |_   _ `.    / \  |  _   _  |  / \    |_   _ \     / \   .' ____ \|_   __  | 
#   | | `. \  / _ \ |_/ | | \_| / _ \     | |_) |   / _ \  | (___ \_| | |_ \_| 
#   | |  | | / ___ \    | |    / ___ \    |  __'.  / ___ \  _.____`.  |  _| _  
#  _| |_.' _/ /   \ \_ _| |_ _/ /   \ \_ _| |__) _/ /   \ \| \____) |_| |__/ | 
# |______.|____| |____|_____|____| |____|_______|____| |____\______.|________|

import sqlite3
from sqlite3 import Error

import classes
import utils

PATH = "../Lap-Time-Prediction/Helper/database.db"

def create_tables(conn: sqlite3.Connection):
    # Create all tables of database
    # :param conn: db connection.
    # :return:

    print("Creating Tables...")

    raise NotImplementedError
    
    try:
        cur = conn.cursor()
        print("Creating vehicles table...")
        cur.execute(vehicles_table)
        print("Creating layout table...")
        cur.execute(layout_table)
        print("Creating dimensions table...")
        cur.execute(dimensions_table)
        print("Creating engine table...")
        cur.execute(engine_table)
        print("Creating trasmission table...")
        cur.execute(trasmission_table)
        print("Creating performance table...")
        cur.execute(performance_table)
        print("Creating overview table...")
        cur.execute(overview_table)
        print("Creating tracks table...")
        cur.execute(tracks_table)
        print("Creating laps table...")
        cur.execute(laps_table)
        print("Creating specs table...")
        cur.execute(specs_table)
        cur.close()

        conn.commit()
        print("Tables created.")
    except Error as e:
        print(e)

def filter(conn: sqlite3.Connection, min_track_laps: int, min_vehicle_laps: int):
    # Create a table from the create_table_sql statement
    # :param conn: db connection.
    # :return:

    print("Creating Views...")

    raise NotImplementedError

    try:
        cur = conn.cursor()
        print("Creating List Cars view...")
        cur.execute(cars)
        # print("Creating List Motorcycles view...")
        # c.execute(motorcycle)
        # print("Creating Track Lap Count view...")
        # c.execute(count_track)
        # print("Creating Vehicle Lap Count view...")
        # c.execute(count_vehicle)
        print("Creating Merge Track List view...")
        cur.execute(extract_track)
        print("Creating Merge Vehicle List view...")
        cur.execute(extract_vehicle)
        print("Creating Merge Lap List view...")
        cur.execute(extract_laps)
        cur.close()
        
        conn.commit()
        print("View created.")
    except Error as e:
        print(e)

def clear_database(conn: sqlite3.Connection):
    # Clear database data
    # :param conn: db connection.
    # :return:

    print("Clearing dataset...")

    del1 = ''' DELETE FROM Laps '''
    del2 = ''' DELETE FROM Tracks '''
    del3 = ''' DELETE FROM Vehicles '''

    try:
        cur = conn.cursor()
        print("Deleting laps table...")
        cur.execute(del1)
        print("Deleting tracks table...")
        cur.execute(del2)
        print("Deleting vehicles table...")
        cur.execute(del3)
        cur.close()
        conn.commit()
        print("Clear complete.")
    except Error as e:
        print(e)

def insert_new_lap(conn: sqlite3, lap: classes.LapTime):
    # Create a new lap into the laps table
    # :param conn: db connection.
    # :param lap: is a lap object.
    # :return: last row id.

    sql = ''' INSERT OR IGNORE INTO Laps(Lap_Time,Driver,Track_ID,Vehicle_ID)
              VALUES(?,?,?,?) '''

    insert_tuple = (lap.lap_time, lap.driver, lap.track.track_id, lap.vehicle.vehicle_id)

    cur = conn.cursor()
    cur.execute(sql, insert_tuple)
    cur.close()

    conn.commit()

    print("Insert: " + str(insert_tuple))
    return cur.lastrowid

def insert_new_track(conn: sqlite3.Connection, track: classes.Track):
    # Create a new track into the tracks table
    # :param conn: db connection.
    # :param track: is a track object.
    # :return: last row id.

    sql = ''' INSERT OR IGNORE INTO Tracks(Track_Name,Country,Total_Length)
              VALUES(?,?,?) '''

    insert_tuple = (track.track_name, track.country, track.total_length)

    cur = conn.cursor()
    cur.execute(sql, insert_tuple)
    cur.close()

    conn.commit()

    print("Insert: " + str(insert_tuple))
    return cur.lastrowid

def insert_new_car(conn: sqlite3.Connection, car: classes.Car):
    # Create a new lap into the vehicles table
    # :param conn: db connection.
    # :param car: is a car object.
    # :return: last row id.

    sql = ''' INSERT OR IGNORE INTO Vehicles(Vehicle_Name,Type)
              VALUES(?,?) '''
    
    insert_tuple = (car.vehicle_name, car.type) 

    cur = conn.cursor()
    cur.execute(sql, insert_tuple)

    curr_id = cur.lastrowid
    
    insert_Layout(conn, curr_id, car.layout)
    insert_dimensions(conn, curr_id, car.dimensions)
    insert_engine(conn, curr_id, car.engine)
    insert_trasmission(conn, curr_id, car.trasmission)
    insert_performance(conn, curr_id, car.performance)
    insert_overview(conn, curr_id, car.overview)

    cur.close()

    conn.commit()

    print("Insert: " + str(insert_tuple))
    return cur.lastrowid

def inser_new_motorcycle(conn: sqlite3.Connection, motorcycle: classes.Motorcycle):
    # Create a new motorcycle into the motorcycle table
    # :param conn: db connection.
    # :param motorcycle: is a motorcycle object.
    # :return: last row id.
    
    sql = ''' INSERT OR IGNORE INTO Vehicles(Vehicle_Name,Type)
              VALUES(?,?) '''
    
    insert_tuple = (motorcycle.vehicle_name, motorcycle.type) 

    cur = conn.cursor()
    cur.execute(sql, insert_tuple)

    raise NotImplementedError

def insert_Layout(conn: sqlite3.Connection, vehicle_id: int, layout: classes.Layout):
    # Create a new layout ref into the layout table
    # :param conn: db connection.
    # :param vehicle_id: id of ref vehicle.
    # :param layout: a layout object.
    # :return: last row id.

    sql = ''' INSERT OR IGNORE INTO Layout(Engine_Layout,Wheel_Drive,Class_Type,Vehicle_ID)
              VALUES(?,?,?,?) '''
    
    insert_tuple = (layout.enigne_layout, layout.wheel_drive, layout.class_type, vehicle_id) 

    cur = conn.cursor()
    cur.execute(sql, insert_tuple)

    cur.close()

    conn.commit()

    print("Insert: " + str(insert_tuple))
    return cur.lastrowid

def insert_dimensions(conn: sqlite3.Connection, vehicle_id: int, dimensions: classes.Dimensions):
    # Create a new dimensions ref into the dimensions table
    # :param conn: db connection.
    # :param vehicle_id: id of ref vehicle.
    # :param dimensions: a dimensions object.
    # :return: last row id.

    sql = ''' INSERT OR IGNORE INTO Dimensions(Curb_Weight,Wheelbase,Long,High,Wide,Vehicle_ID)
              VALUES(?,?,?,?,?,?) '''
    
    insert_tuple = (dimensions.curb_weight, dimensions.wheelbase, dimensions.long, dimensions.high, dimensions.wide, vehicle_id) 

    cur = conn.cursor()
    cur.execute(sql, insert_tuple)

    cur.close()

    conn.commit()

    print("Insert: " + str(insert_tuple))
    return cur.lastrowid

def insert_engine(conn: sqlite3.Connection, vehicle_id: int, engine: classes.Engine):
    # Create a new engine ref into the engine table
    # :param conn: db connection.
    # :param vehicle_id: id of ref vehicle.
    # :param engine: a engine object.
    # :return: last row id.

    sql = ''' INSERT OR IGNORE INTO Engine(Engine,Displacement,Power,Torque,Vehicle_ID)
              VALUES(?,?,?,?,?) '''
    
    insert_tuple = (engine.engine, engine.displacement, engine.power, engine.torque, vehicle_id)

    cur = conn.cursor()
    cur.execute(sql, insert_tuple)

    cur.close()

    conn.commit()

    print("Insert: " + str(insert_tuple))
    return cur.lastrowid

def insert_trasmission(conn: sqlite3.Connection, vehicle_id: int, trasmission: classes.Trasmission):
    # Create a new trasmission ref into the trasmission table
    # :param conn: db connection.
    # :param vehicle_id: id of ref vehicle.
    # :param trasmission: a trasmission object.
    # :return: last row id.

    sql = ''' INSERT OR IGNORE INTO Trasmission(Trasmission_Name,Trasmission_Type,N_Trasmission,Vehicle_ID)
              VALUES(?,?,?,?) '''
    
    insert_tuple = (trasmission.trasmission_name, trasmission.trasmission_type, trasmission.n_trasmission, vehicle_id)

    cur = conn.cursor()
    cur.execute(sql, insert_tuple)

    cur.close()

    conn.commit()

    print("Insert: " + str(insert_tuple))
    return cur.lastrowid

def insert_performance(conn: sqlite3.Connection, vehicle_id: int, performance: classes.Performance):
    # Create a new performance ref into the performance table
    # :param conn: db connection.
    # :param vehicle_id: id of ref vehicle.
    # :param performance: a performance object.
    # :return: last row id.

    sql = ''' INSERT OR IGNORE INTO Performance(Zero_Hundred,Break_Distance,Top_Speed,Vehicle_ID)
              VALUES(?,?,?,?) '''
    
    insert_tuple = (performance.zero_hundred, performance.break_distance, performance.top_speed, vehicle_id) 

    cur = conn.cursor()
    cur.execute(sql, insert_tuple)

    cur.close()

    conn.commit()

    print("Insert: " + str(insert_tuple))
    return cur.lastrowid

def insert_overview(conn: sqlite3.Connection, vehicle_id: int, overview: classes.Overview):
    # Create a new overview ref into the overview table
    # :param conn: db connection.
    # :param vehicle_id: id of ref vehicle.
    # :param overview: a layout overview.
    # :return: last row id.

    sql = ''' INSERT OR IGNORE INTO Overview(Manufacturer,Origin_Country,Introduced_Year,Vehicle_ID)
              VALUES(?,?,?,?) '''
    
    insert_tuple = (overview.manufacturer, overview.origin_country, overview.introduced_year, vehicle_id) 

    cur = conn.cursor()
    cur.execute(sql, insert_tuple)

    cur.close()

    conn.commit()

    print("Insert: " + str(insert_tuple))
    return cur.lastrowid

def get_all_laps(conn: sqlite3.Connection):
    # Get all laps from the laps table
    # :param conn: db connection.
    # :return: list of all record.
    
    print("Getting all laps data...")

    sql = ''' SELECT * FROM Laps '''
              
    cur = conn.cursor()
    cur.execute(sql)

    output = cur.fetchall()
    cur.close()

    print("SELECT all laps complete.")
    return output
    
def get_all_tracks(conn: sqlite3.Connection):
    # Get all tracks from the tracks table
    # :param conn: db connection.
    # :return: list of all record.

    print("Getting all traks data...")

    sql = ''' SELECT * FROM Tracks '''
              
    cur = conn.cursor()
    cur.execute(sql)

    output = cur.fetchall()
    cur.close()

    print("SELECT all tracks complete.")
    return output

def get_all_vehicles_specs(conn: sqlite3.Connection):
    # Get all vehicles from the vehicles table join all specs
    # :param conn: db connection.
    # :return: list of all record.

    print("Getting all vehicles data...")

    sql = ''' SELECT * FROM Vehicles 
            JOIN Layout ON Vehicles.Vehicle_ID = Layout.Vehicle_ID
            JOIN Dimensions ON Vehicles.Vehicle_ID = Dimensions.Vehicle_ID
            JOIN Engine ON Vehicles.Vehicle_ID = Engine.Vehicle_ID
            JOIN Trasmission ON Vehicles.Vehicle_ID = Trasmission.Vehicle_ID
            JOIN Performance ON Vehicles.Vehicle_ID = Performance.Vehicle_ID
            JOIN Overview ON Vehicles.Vehicle_ID = Overview.Vehicle_ID '''
              
    cur = conn.cursor()
    cur.execute(sql)

    output = cur.fetchall()
    cur.close()
    
    print("SELECT all vehicles complete.")
    return output

def get_all_vehicles(conn: sqlite3.Connection):
    # Get all vehicles from the vehicles table
    # :param conn: db connection.
    # :return: list of all record.

    print("Getting all vehicles data...")

    sql = ''' SELECT * FROM Vehicles '''
              
    cur = conn.cursor()
    cur.execute(sql)

    output = cur.fetchall()
    cur.close()
    
    print("SELECT all vehicles complete.")
    return output

def get_specific_lap(conn: sqlite3.Connection, track_id: int, vehicle_id: int):
    # Get specific laptime  from the laps table
    # :param conn: db connection.
    # :param track_name: track name string.
    # :param vehicle_name: vehicle name string.
    # :return: list of all specific record.

    sql = ''' SELECT * FROM Laps WHERE (Tracks_ID = ?) AND (Vehicle_ID = ?)  '''
              
    cur = conn.cursor()
    cur.execute(sql, (track_id, vehicle_id))

    output = cur.fetchall()
    cur.close()

    print("SELECT specific lap complete.")
    return output
    
def get_specific_track(conn: sqlite3.Connection, track_id: int, track_name: str):
    # Get specific trakcs from the tracks table
    # :param conn: db connection.
    # :param tracks_name: track name string.
    # :return: list of all specific record.

    by_id = "Tracks_ID = ?"
    by_name = "Tracks_Name = ?"
              
    if (track_id != -1):
        sql = f''' SELECT * FROM Tracks WHERE {by_id} '''
    else:
        sql = f''' SELECT * FROM Tracks WHERE {by_name} '''

    cur = conn.cursor()
    cur.execute(sql, (track_id, track_name))

    output = cur.fetchall()
    cur.close()

    print("SELECT specific track complete.")
    return output

def get_specific_vehicle_specs(conn: sqlite3.Connection, vehicle_id: int,  vehicle_name: str):
    # Get specific vehicles from the vehicles table join all specs
    # :param conn: db connection.
    # :param vehicle_name: vehicle name string.
    # :return: list of all specific record.

    by_id = "Vehicle_ID = ? "
    by_name = "Vehicle_Name = ?"

    cur = conn.cursor()

    joins = ''' JOIN Layout ON Vehicles.Vehicle_ID = Layout.Vehicle_ID
                JOIN Dimensions ON Vehicles.Vehicle_ID = Dimensions.Vehicle_ID
                JOIN Engine ON Vehicles.Vehicle_ID = Engine.Vehicle_ID
                JOIN Trasmission ON Vehicles.Vehicle_ID = Trasmission.Vehicle_ID
                JOIN Performance ON Vehicles.Vehicle_ID = Performance.Vehicle_ID
                JOIN Overview ON Vehicles.Vehicle_ID = Overview.Vehicle_ID '''
    
    if (vehicle_id != -1):
        sql = f''' SELECT * FROM Vehicles 
        {joins} 
        WHERE {by_id} '''
        cur.execute(sql, (vehicle_id, ))
    else:
        sql = f''' SELECT * FROM Vehicles
        {joins} 
        WHERE {by_name} '''
        cur.execute(sql, (vehicle_name, ))

    cur.close()

    output = cur.fetchall()
    
    print("SELECT specific vehicle complete.")
    return output

def get_specific_vehicle(conn: sqlite3.Connection, vehicle_id: int, vehicle_name: str):
    # Get specific vehicles from the vehicles table
    # :param conn: db connection.
    # :param vehicle_name: vehicle name string.
    # :return: list of all specific record.

    by_id = "Vehicle_ID = ?"
    by_name = "Vehicle_Name = ?"
    
    cur = conn.cursor()

    if (vehicle_id != -1):
        sql = f''' SELECT * FROM Vehicles WHERE {by_id} '''
        cur.execute(sql, (vehicle_id, ))
    else:
        sql = f''' SELECT * FROM Vehicles WHERE {by_name} '''
        cur.execute(sql, (vehicle_name, ))

    cur.close()

    output = cur.fetchall()
    
    print("SELECT specific vehicle complete.")
    return output

def delete_specific_lap(conn: sqlite3.Connection, track_id: int, vehicle_id: int):
    # Delete a lap by track name and vehicle name
    # :param conn: db connection.
    # :param track_name: track name string.
    # :param vehicle_name: vehicle name string.
    # :return:
    
    sql = ''' DELETE FROM Laps WHERE (Track_ID = ?) AND (Vehicle_ID = ?) '''
    cur = conn.cursor()
    cur.execute(sql, (track_id, vehicle_id))
    cur.close()

    conn.commit()

    print("Delete: " + sql)
    
def delete_specific_track(conn: sqlite3.Connection, track_id: int, track_name: str):
    # Delete a track by track name
    # :param conn: db connection.
    # :param track_name: track name string.
    # :return:
    
    by_id = "Tracks_ID = ?"
    by_name = "Tracks_Name = ?"
              
    if (track_id != -1):
        sql = f''' DELETE FROM Tracks WHERE {by_id} '''
    else:
        sql = f''' DELETE FROM Tracks WHERE {by_name} '''

    cur = conn.cursor()
    cur.execute(sql, (track_id, track_name))
    cur.close()

    conn.commit()

    print("Delete: " + track_name)

def delete_specific_vehicle(conn: sqlite3.Connection, vehicle_id: int, vehicle_name: str):
    # Delete a vehicle by vehicle name
    # :param conn: db connection.
    # :param vehicle_id: vehicle id.
    # :param vehicle_name: vehicle name string.
    # :return:
    
    by_id = "Vehicle_ID = ?"
    by_name = "Vehicle_Name = ?"

    if (vehicle_id != -1):
        sql = f''' DELETE FROM Vehicles WHERE {by_id} '''
    else:
        sql = f''' DELETE FROM Vehicles WHERE {by_name} '''

    cur = conn.cursor()
    cur.execute(sql, (vehicle_id, vehicle_name))
    cur.close()

    conn.commit()

    print("Delete: " + vehicle_name)

def update_specific_lap(conn: sqlite3.Connection, track_id: int, vehicle_id: int, values: tuple):
    # Update a vehicle by track name and vehicle name
    # :param conn: db connection.
    # :param track_id: track id.
    # :param vehicle_id: vehicle id.
    # :return: number of updatetd row.

    raise NotImplementedError
    
def update_specific_track(conn: sqlite3.Connection, track_id: int, track_name: str, values: tuple):
    # Update a vehicle by track name
    # :param conn: db connection.
    # :param vehicle_name: vehicle name string.
    # :return: number of updatetd row.

    raise NotImplementedError

def update_specific_vehicle(conn: sqlite3.Connection, vehicle_id: int, vehicle_name: str, values: tuple):
    # Update a vehicle by vehicle name
    # :param conn: db connection.
    # :param vehicle_id: vehicle id.
    # :return: number of updatetd row.

    raise NotImplementedError
