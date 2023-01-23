#  ______   _____  _____  ____    ____  _______   
# |_   _ `.|_   _||_   _||_   \  /   _||_   __ \  
#   | | `. \ | |    | |    |   \/   |    | |__) | 
#   | |  | | | '    ' |    | |\  /| |    |  ___/  
#  _| |_.' /  \ \__/ /    _| |_\/_| |_  _| |_     
# |______.'    `.__.'    |_____||_____||_____|  

import sqlite3
from sqlite3 import Error

import utils

PATH = "../Lap-Time-Prediction/Fastestlaps/dump/dump.db"

def create_tables(conn: sqlite3.Connection):
    # Create all tables of database
    # :param conn: db connection.
    # :return:

    print("Creating Tables...")

    vehicles_table = '''CREATE TABLE IF NOT EXISTS "Vehicles" (
	"Vehicle_Name"  TEXT NOT NULL UNIQUE,
	"HRef"          TEXT,
	PRIMARY KEY("Vehicle_Name")
    )'''

    tracks_table = '''CREATE TABLE IF NOT EXISTS "Tracks" (
	"Track_Name"    TEXT NOT NULL UNIQUE,
	"HRef"          TEXT,
    "Country"       TEXT,
	"Total_Length"  REAL,
	PRIMARY KEY("Track_Name")
    )'''

    laps_table = '''CREATE TABLE IF NOT EXISTS "Laps" (
	"Lap_Time"	REAL NOT NULL,
	"Driver"	TEXT,
	"PS_KG"	    TEXT,
	"Track"	    TEXT NOT NULL,
	"Vehicle"	TEXT NOT NULL,
	FOREIGN KEY("Track") REFERENCES "Tracks"("Track_Name") ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY("Vehicle") REFERENCES "Vehicles"("Vehicle_Name") ON DELETE CASCADE ON UPDATE CASCADE
    )'''

    specs_table = '''CREATE TABLE IF NOT EXISTS "Specs" (
	"Vehicle"	        TEXT NOT NULL,
    "Manufacturer"      TEXT,
	"Type"	            TEXT,
	"Type_Usage"	    TEXT,
    "Introduced_Year"   INTEGER,
    "Country"	        TEXT,
	"Curb_Weight"	    REAL,
	"Wheelbase"	        REAL,
	"Dim_Long"	        REAL,
	"Dim_Wide"	        REAL,
	"Dim_High"	        REAL,
	"Zero_Hundred"	    REAL,
	"Hundred_Zero"	    REAL,
	"Top_Speed"	        INTEGER,
	"Engine_Type"	    TEXT,
	"Displacement"	    REAL,
	"Power_PS"	        INTEGER,
	"Power_BHP"	        INTEGER,
	"Power_KW"	        INTEGER,
	"Torque"	        INTEGER,
	"Power_Weight"	    INTEGER,
	"Torque_Weight"	    INTEGER,
	"Efficiency"	    INTEGER,
	"Trasmission"	    TEXT,
	"Layout"	        TEXT,
	FOREIGN KEY("Vehicle") REFERENCES "Vehicles"("Vehicle_Name") ON DELETE CASCADE ON UPDATE CASCADE
    )'''
    
    try:
        cur = conn.cursor()
        print("Creating vehicles table...")
        cur.execute(vehicles_table)
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

    cars = '''
    CREATE TEMP VIEW List_Cars
    AS
    SELECT * FROM Specs
    WHERE Specs.Type = 'Car'
    '''

    # motorcycle = '''
    # CREATE TEMP VIEW List_Motorcycles
    # AS
    # SELECT * FROM Specs
    # WHERE Specs.Type = 'Motorcycle'
    # '''
    #
    # count_track = '''
    # CREATE TEMP VIEW Track_Lap_Count
    # AS
    # SELECT
    #     Laps.Track, COUNT(Laps.Vehicle)
    # FROM
    #     Laps INNER JOIN List_Cars ON Laps.Vehicle = List_Cars.Vehicle
    # GROUP BY
    #     Laps.Track
    # ORDER BY
    #     Laps.Track ASC
    # '''
    #
    # count_vehicle = '''
    # CREATE TEMP VIEW Vehicle_Lap_Count
    # AS
    # SELECT
    #     List_Cars.Vehicle, COUNT(Laps.Track)
    # FROM
    #     Laps INNER JOIN List_Cars ON Laps.Vehicle = List_Cars.Vehicle
    # GROUP BY
    #     List_Cars.Vehicle
    # ORDER BY
    #     List_Cars.Vehicle ASC
    # '''

    extract_track = f'''
    CREATE TEMP VIEW Extract_Track_List
    AS
    SELECT
        Tracks.Track_Name, Tracks.Country, Tracks.Total_Length
    FROM
        Laps JOIN List_Cars ON Laps.Vehicle = List_Cars.Vehicle
        JOIN Tracks ON Laps.Track = Tracks.Track_Name
    GROUP BY
        Laps.Track
    HAVING
        COUNT(DISTINCT Laps.Vehicle) >= {min_track_laps}
    ORDER BY
        Laps.Track ASC
    '''

    extract_vehicle = f'''
    CREATE TEMP VIEW Extract_Vehicle_List
    AS
    SELECT
        List_Cars.*
    FROM
        Laps JOIN List_Cars ON Laps.Vehicle = List_Cars.Vehicle
        JOIN Tracks ON Laps.Track = Tracks.Track_Name
    GROUP BY
        Laps.Vehicle
    HAVING
        COUNT(Laps.Track) >= {min_vehicle_laps}
    ORDER BY
        Laps.Vehicle ASC
    '''
    
    extract_laps = '''
    CREATE TEMP VIEW Extract_Laps_List
    AS
    SELECT
        Laps.*
    FROM
        Laps JOIN Extract_Vehicle_List AS EVL ON Laps.Vehicle = EVL.Vehicle
        JOIN Extract_Track_List AS ETL ON Laps.Track = ETL.Track_Name
    ORDER BY
        Laps.Track ASC
    '''

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
    del3 = ''' DELETE FROM Specs '''
    del4 = ''' DELETE FROM Vehicles '''

    try:
        cur = conn.cursor()
        print("Deleting laps table...")
        cur.execute(del1)
        print("Deleting tracks table...")
        cur.execute(del2)
        print("Deleting specs table...")
        cur.execute(del3)
        print("Deleting vehicles table...")
        cur.execute(del4)
        cur.close()
        conn.commit()
        print("Clear complete.")
    except Error as e:
        print(e)

def insert_new_lap(conn: sqlite3.Connection, lap):
    # Create a new lap into the laps table
    # :param conn: db connection.
    # :param lap: is a tuple.
    # :return: last row id.

    sql = ''' INSERT OR IGNORE INTO Laps(Lap_Time,Driver,PS_KG,Track,Vehicle)
              VALUES(?,?,?,?,?) '''

    cur = conn.cursor()
    cur.execute(sql, lap)
    cur.close()

    conn.commit()

    print("Insert: " + str(lap))
    return cur.lastrowid

def insert_new_track(conn: sqlite3.Connection, track):
    # Create a new track into the tracks table
    # :param conn: db connection.
    # :param track: is a tuple.
    # :return: last row id.

    sql = ''' INSERT OR IGNORE INTO Tracks(Track_Name,HRef,Country,Total_Length)
              VALUES(?,?,?,?) '''
              
    cur = conn.cursor()
    cur.execute(sql, track)
    cur.close()

    conn.commit()

    print("Insert: " + str(track))
    return cur.lastrowid

def insert_new_specs(conn: sqlite3.Connection, specs):
    # Create a new specs into the specs table
    # :param conn: db connection.
    # :param specs: is a tuple.
    # :return: last row id.

    sql = ''' INSERT OR IGNORE INTO Specs(Vehicle,Manufacturer,Type,Type_Usage,Introduced_Year,Country,
    Curb_Weight,Wheelbase,Dim_Long,Dim_Wide,Dim_High,Zero_Hundred,Hundred_Zero,Top_Speed,
    Engine_Type,Displacement,Power_PS,Power_BHP,Power_KW,Torque,
    Power_Weight,Torque_Weight,Efficiency,Trasmission,Layout)
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''

    cur = conn.cursor()
    cur.execute(sql, specs)
    cur.close()

    conn.commit()

    print("Insert: " + str(specs))
    return cur.lastrowid

def insert_new_vehicle(conn: sqlite3.Connection, vehicle):
    # Create a new vehicle into the vehicles table
    # :param conn: db connection.
    # :param vehicle: is a tuple.
    # :return: last row id.

    sql = ''' INSERT OR IGNORE INTO Vehicles(Vehicle_Name,Href)
              VALUES(?,?) '''
              
    cur = conn.cursor()
    cur.execute(sql, vehicle)
    cur.close()

    conn.commit()

    print("Insert: " + str(vehicle))
    return cur.lastrowid

def insert_new_record(lap: tuple, track: tuple, vehicle: tuple):
    conn = utils.get_SQLite_connection()
    insert_new_vehicle(conn,vehicle)
    insert_new_track(conn,track)
    insert_new_lap(conn,lap)
    conn.close()

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

def get_all_specs(conn: sqlite3.Connection):
    # Get all specs from the specs table
    # :param conn: db connection.
    # :return: list of all record.
    
    print("Getting all laps data...")

    sql = ''' SELECT * FROM Specs '''
              
    cur = conn.cursor()
    cur.execute(sql)

    output = cur.fetchall()
    cur.close()

    print("SELECT all laps complete.")
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
