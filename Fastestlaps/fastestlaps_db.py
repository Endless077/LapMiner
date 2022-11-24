# Fastestlaps database

import sqlite3
from sqlite3 import Error

PATH = "./scrap.db"

def create_database():
    # Create a connection to db
    # :param:
    # :return: connection object or None.
    
    print("Version Database:" + sqlite3.version)
    print("Creating " + PATH + "...")

    conn = None
    try:
        conn = sqlite3.connect(PATH)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def get_connection():
    # Create a database connection to the SQLite database specified by db_file
    # :param db_file: database file.
    # :return: connection object or None.

    print("Getting database connection...")

    conn = None
    try:
        conn = sqlite3.connect(PATH)
        return conn
    except Error as e:
        print(e)

    return conn

def create_tables(conn):
    # Create a table from the create_table_sql statement
    # :param conn: db connection.
    # :return:

    print("Creating Tables...")

    vehicles_table = '''CREATE TABLE IF NOT EXISTS "Vehicles" (
	"Vehicle_Name"  TEXT NOT NULL UNIQUE,
	"HRef"          TEXT NOT NULL,
	PRIMARY KEY("Vehicle_Name")
    )'''

    tracks_table = '''CREATE TABLE IF NOT EXISTS "Tracks" (
	"Track_Name"    TEXT NOT NULL UNIQUE,
	"HRef"          TEXT NOT NULL,
    "Country"       TEXT NOT NULL,
	"Total_Length"  REAL NOT NULL,
	PRIMARY KEY("Track_Name")
    )'''

    laps_table = '''CREATE TABLE IF NOT EXISTS "Laps" (
	"Lap_Time"  REAL NOT NULL,
	"Driver"    TEXT NOT NULL,
	"PS_KG"     TEXT NOT NULL,
	"Track"     TEXT NOT NULL,
	"Vehicle"	TEXT NOT NULL,
	FOREIGN KEY("Track") REFERENCES "Tracks"("Track_Name") ON DELETE CASCADE,
    FOREIGN KEY("Vehicle") REFERENCES "Vehicles"("Vehicle_Name") ON DELETE CASCADE
    )'''

    try:
        c = conn.cursor()
        print("Creating vehicles table...")
        c.execute(vehicles_table)
        print("Creating tracks table...")
        c.execute(tracks_table)
        print("Creating laps table...")
        c.execute(laps_table)
        print("Table created.")
    except Error as e:
        print(e)

def clear_database(conn):
    # Clear database data
    # :param conn: db connection.
    # :return:

    print("Clearing dataset...")

    del1 = ''' DELETE FROM Laps '''
    del2 = ''' DELETE FROM Tracks '''
    del3 = ''' DELETE FROM Vehicles '''

    try:
        c = conn.cursor()
        print("Deleting laps table...")
        c.execute(del1)
        print("Deleting tracks table...")
        c.execute(del2)
        print("Deleting vehicles table...")
        c.execute(del3)
        conn.commit()
        print("Clear complete.")
    except Error as e:
        print(e)

def insert_new_lap(conn, lap):
    # Create a new lap into the laps table
    # :param conn: db connection.
    # :param lap: is a tuple.
    # :return: last row id.

    sql = ''' INSERT OR IGNORE INTO Laps(Lap_Time,Driver,PS_KG,Track,Vehicle)
              VALUES(?,?,?,?,?) '''

    cur = conn.cursor()
    cur.execute(sql, lap)
    conn.commit()

    print("Insert: " + str(lap))
    return cur.lastrowid

def insert_new_track(conn, track):
    # Create a new lap into the laps table
    # :param conn: db connection.
    # :param track: is a tuple.
    # :return: last row id.

    sql = ''' INSERT OR IGNORE INTO Tracks(Track_Name,HRef,Country,Total_Length)
              VALUES(?,?,?,?) '''
              
    cur = conn.cursor()
    cur.execute(sql, track)
    conn.commit()

    print("Insert: " + str(track))
    return cur.lastrowid

def insert_new_vehichle(conn, vehicle):
    # Create a new lap into the laps table
    # :param conn: db connection.
    # :param vehicle: is a tuple.
    # :return: last row id.

    sql = ''' INSERT OR IGNORE INTO Vehicles(Vehicle_Name,Href)
              VALUES(?,?) '''
              
    cur = conn.cursor()
    cur.execute(sql, vehicle)
    conn.commit()

    print("Insert: " + str(vehicle))
    return cur.lastrowid

def insert_new_record(lap, track, vehicle):
    conn = get_connection()
    insert_new_vehichle(conn,vehicle)
    insert_new_track(conn,track)
    insert_new_lap(conn,lap)

def get_all_laps(conn):
    # Get all laps from the laps table
    # :param conn: db connection.
    # :return: list of all record.
    
    print("Getting all laps data...")

    sql = ''' SELECT * FROM Laps '''
              
    cur = conn.cursor()
    cur.execute(sql)

    output = cur.fetchall()

    print("SELECT all laps complete.")
    return output
    
def get_all_tracks(conn):
    # Get all tracks from the tracks table
    # :param conn: db connection.
    # :return: list of all record.

    print("Getting all traks data...")

    sql = ''' SELECT * FROM Tracks '''
              
    cur = conn.cursor()
    cur.execute(sql)

    output = cur.fetchall()

    print("SELECT all tracks complete.")
    return output

def get_all_vehicles(conn):
    # Get all vehicles from the vehicles table
    # :param conn: db connection.
    # :return: list of all record.

    print("Getting all vehicles data...")

    sql = ''' SELECT * FROM Vehicles '''
              
    cur = conn.cursor()
    cur.execute(sql)

    output = cur.fetchall()

    print("SELECT all vehicles complete.")
    return output

def get_specific_lap(conn, track_name, vehicle_name):
    # Get specific laptime  from the laps table
    # :param conn: db connection.
    # :param track_name: track name string.
    # :param vehicle_name: vehicle name string.
    # :return: list of all specific record.

    print("Getting " + track_name + " and " + vehicle_name + " lap data...")

    sql = ''' SELECT * FROM Laps WHERE Track = ? AND Vehicle = ? '''
              
    cur = conn.cursor()
    cur.execute(sql, (track_name, vehicle_name))

    output = cur.fetchall()

    print("SELECT specific lap complete.")
    return output
    
def get_specific_track(conn, track_name):
    # Get specific trakcs from the tracks table
    # :param conn: db connection.
    # :param tracks_name: track name string.
    # :return: list of all specific record.

    print("Getting " + track_name +" track data...")

    sql = ''' SELECT * FROM Vehicles WHERE Track_Name = ? '''
              
    cur = conn.cursor()
    cur.execute(sql, (track_name, ))

    output = cur.fetchall()

    print("SELECT specific track complete.")
    return output

def get_specific_vehicle(conn, vehicle_name):
    # Get specific vehicles from the vehicles table
    # :param conn: db connection.
    # :param vehicle_name: vehicle name string.
    # :return: list of all specific record.

    print("Getting " + vehicle_name +" vehicle data...")

    sql = ''' SELECT * FROM Vehicles WHERE Vehicle_Name = ? '''
              
    cur = conn.cursor()
    cur.execute(sql, (vehicle_name, ))

    output = cur.fetchall()

    print("SELECT specific vehicle complete.")
    return output

def delete_specific_lap(conn, track_name, vehicle_name):
    # Delete a lap by track name and vehicle name
    # :param conn: db connection.
    # :param track_name: track name string.
    # :param vehicle_name: vehicle name string.
    # :return:
    
    sql = ''' DELETE FROM Laps WHERE Track = ? AND Vehicle = ? '''
    cur = conn.cursor()
    cur.execute(sql, (track_name, vehicle_name))
    conn.commit()

    print("Delete: " + sql)
    
def delete_specific_track(conn, track_name):
    # Delete a track by track name
    # :param conn: db connection.
    # :param track_name: track name string.
    # :return:
    
    sql = ''' DELETE FROM Tracks WHERE Track_Name = ? '''
    cur = conn.cursor()
    cur.execute(sql, (track_name,))
    conn.commit()

    print("Delete: " + track_name)

def delete_specific_vehicle(conn, vehicle_name):
    # Delete a vehicle by vehicle name
    # :param conn: db connection.
    # :param vehicle_name: vehicle name string.
    # :return:
    
    sql = ''' DELETE FROM Vehicles WHERE Vehicles_Name = ? '''
    cur = conn.cursor()
    cur.execute(sql, (vehicle_name,))
    conn.commit()

    print("Delete: " + vehicle_name)

def update_specific_lap(conn, track_name, vehicle_name, values):
    # Delete a vehicle by track name and vehicle name
    # :param conn: db connection.
    # :param track_name: track name string.
    # :param vehicle_name: vehicle name string.
    # :return: number of updatetd row.

    raise NotImplementedError
    
def update_specific_track(conn, track_name, values):
    # Delete a vehicle by track name
    # :param conn: db connection.
    # :param vehicle_name: vehicle name string.
    # :return: number of updatetd row.

    raise NotImplementedError

def update_specific_vehicle(conn, vehicle_name, values):
    # Delete a vehicle by vehicle name
    # :param conn: db connection.
    # :param vehicle_name: vehicle name string.
    # :return: number of updatetd row.

    raise NotImplementedError
