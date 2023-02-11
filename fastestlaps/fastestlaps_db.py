#  ______   _____  _____  ____    ____  _______   
# |_   _ `.|_   _||_   _||_   \  /   _||_   __ \  
#   | | `. \ | |    | |    |   \/   |    | |__) | 
#   | |  | | | '    ' |    | |\  /| |    |  ___/  
#  _| |_.' /  \ \__/ /    _| |_\/_| |_  _| |_     
# |______.'    `.__.'    |_____||_____||_____|  

import re
import sqlite3
from sqlite3 import Error

import utils

FOLDER = "../LapMiner/fastestlaps/dump/"
PATH = "../LapMiner/fastestlaps/dump/dump.db"

def create_tables(conn: sqlite3.Connection):
    # Create all tables of database
    # :param conn: db connection.
    # :return:

    print("Creating Tables...")

    vehicles_table = '''CREATE TABLE IF NOT EXISTS "VEHICLES" (
	"vehicle_name"  TEXT NOT NULL UNIQUE,
	"href"          TEXT,
	PRIMARY KEY("vehicle_name")
    )'''

    tracks_table = '''CREATE TABLE IF NOT EXISTS "TRACKS" (
	"track_name"    TEXT NOT NULL UNIQUE,
	"href"          TEXT,
    "country"       TEXT,
	"total_length"  REAL,
	PRIMARY KEY("track_name")
    )'''

    laps_table = '''CREATE TABLE IF NOT EXISTS "LAPS" (
	"lap_time"	REAL NOT NULL,
	"driver"	TEXT,
	"ps_kg"	    TEXT,
	"track"	    TEXT NOT NULL,
	"vehicle"	TEXT NOT NULL,
	FOREIGN KEY("track") REFERENCES "TRACKS"("track_name") ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY("vehicle") REFERENCES "VEHICLES"("vehicle_name") ON DELETE CASCADE ON UPDATE CASCADE
    )'''

    specs_table = '''CREATE TABLE IF NOT EXISTS "SPECS" (
	"vehicle"	        TEXT NOT NULL,
    "manufacturer"      TEXT,
    "model"             TEXT,
	"type"	            TEXT,
	"type_usage"	    TEXT,
    "introduced_year"   INTEGER,
    "country"	        TEXT,
	"curb_weight"	    REAL,
	"wheelbase"	        REAL,
	"dim_long"	        REAL,
	"dim_wide"	        REAL,
	"dim_high"	        REAL,
	"zero_hundred"	    REAL,
	"hundred_zero"	    REAL,
	"top_speed"	        INTEGER,
	"engine_type"	    TEXT,
	"displacement"	    REAL,
	"power_ps"	        INTEGER,
	"power_bhp"	        INTEGER,
	"power_kw"	        INTEGER,
	"torque"	        INTEGER,
	"power_weight"	    INTEGER,
	"torque_weight"	    INTEGER,
	"efficiency"	    INTEGER,
	"trasmission"	    TEXT,
	"layout"	        TEXT,
	FOREIGN KEY("vehicle") REFERENCES "VEHICLES"("vehicle_name") ON DELETE CASCADE ON UPDATE CASCADE
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

def clear_database(conn: sqlite3.Connection):
    # Clear database data
    # :param conn: db connection.
    # :return:

    print("Clearing dataset...")

    del1 = ''' DELETE FROM LAPS '''
    del2 = ''' DELETE FROM TRACKS '''
    del3 = ''' DELETE FROM SPECS '''
    del4 = ''' DELETE FROM VEHICLES '''

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

def insert_new_lap(conn: sqlite3.Connection, lap: tuple):
    # Create a new lap into the laps table
    # :param conn: db connection.
    # :param lap: is a tuple.
    # :return: last row id.

    sql = ''' INSERT OR IGNORE INTO LAPS(lap_time,driver,ps_kg,track,vehicle)
              VALUES(?,?,?,?,?) '''

    cur = conn.cursor()
    cur.execute(sql, lap)
    cur.close()

    conn.commit()

    print("Insert: " + str(lap))
    return cur.lastrowid

def insert_new_track(conn: sqlite3.Connection, track: tuple):
    # Create a new track into the tracks table
    # :param conn: db connection.
    # :param track: is a tuple.
    # :return: last row id.

    sql = ''' INSERT OR IGNORE INTO TRACKS(track_name,href,country,total_length)
              VALUES(?,?,?,?) '''
              
    cur = conn.cursor()
    cur.execute(sql, track)
    cur.close()

    conn.commit()

    print("Insert: " + str(track))
    return cur.lastrowid

def insert_new_specs(conn: sqlite3.Connection, specs: tuple):
    # Create a new specs into the specs table
    # :param conn: db connection.
    # :param specs: is a tuple.
    # :return: last row id.

    sql = ''' INSERT OR IGNORE INTO SPECS(vehicle,manufacturer,model,type,type_usage,introduced_year,country,
    curb_weight,wheelbase,dim_long,dim_wide,dim_high,zero_hundred,hundred_zero,top_speed,
    engine_type,displacement,power_ps,power_bhp,power_kw,torque,
    power_weight,torque_weight,efficiency,trasmission,layout)
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''

    cur = conn.cursor()
    cur.execute(sql, specs)
    cur.close()

    conn.commit()

    print("Insert: " + str(specs))
    return cur.lastrowid

def insert_new_vehicle(conn: sqlite3.Connection, vehicle: tuple):
    # Create a new vehicle into the vehicles table
    # :param conn: db connection.
    # :param vehicle: is a tuple.
    # :return: last row id.

    sql = ''' INSERT OR IGNORE INTO VEHICLES(vehicle_name,href)
              VALUES(?,?) '''
              
    cur = conn.cursor()
    cur.execute(sql, vehicle)
    cur.close()

    conn.commit()

    print("Insert: " + str(vehicle))
    return cur.lastrowid

def insert_new_record(lap: tuple, track: tuple, vehicle: tuple):
    # Insert a new record (Lap, Track, Vehicle)
    # :param lap: a tuple record of laptime.
    # :param track: a tuple record of track.
    # :param vehicle: a tuple record of vehicle.

    conn = utils.get_SQLite_connection(PATH)
    insert_new_vehicle(conn,vehicle)
    insert_new_track(conn,track)
    insert_new_lap(conn,lap)
    conn.close()

def get_all_laps(conn: sqlite3.Connection):
    # Get all laps from the laps table
    # :param conn: db connection.
    # :return: list of all record.
    
    print("Getting all laps data...")

    sql = ''' SELECT * FROM LAPS '''
              
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

    sql = ''' SELECT * FROM TRACKS '''
              
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

    sql = ''' SELECT * FROM SPECS '''
              
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

    sql = ''' SELECT * FROM VEHICLES '''
              
    cur = conn.cursor()
    cur.execute(sql)

    output = cur.fetchall()
    cur.close()
    
    print("SELECT all vehicles complete.")
    return output

def update_specific_lap(conn: sqlite3.Connection, track_name: int, vehicle_name: int, values: dict):
    # Update a lap by track name and vehicle name
    # :param conn: db connection.
    # :param track_name: track name string.
    # :param vehicle_name: vehicle name string.
    # :param values: a dict with key are the column list to set and values are the new values set.
    # :return:

    raise NotImplementedError
    
def update_specific_track(conn: sqlite3.Connection, track_name: str, values: dict):
    # Update a track by track name
    # :param conn: db connection.
    # :param track_name: track name string.
    # :param values: a dict with key are the column list to set and values are the new values set.
    # :return:

    raise NotImplementedError

def update_specific_vehicle(conn: sqlite3.Connection, vehicle_name: str, values: dict):
    # Update a vehicle by vehicle name
    # :param conn: db connection.
    # :param vehicle_name: vehicle name string.
    # :param values: a dict with key are the column list to set and values are the new values set.
    # :return:

    raise NotImplementedError
