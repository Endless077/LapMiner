# Fastestlaps database

import sqlite3
from sqlite3 import Error

PATH = "./scrap.db"

def create_database():
    # Create a connection to db
    
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
    # :param db_file: database file
    # :return: Connection object or None

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
    # :param conn: Connection object
    # :param create_table_sql: a CREATE TABLE statement
    # :return:

    print("Creating Tables...")

    vehicles_table = '''CREATE TABLE IF NOT EXISTS "Vehicles" (
	"Vehicle_Name"	TEXT NOT NULL UNIQUE,
	"HRef"	TEXT NOT NULL,
	PRIMARY KEY("Vehicle_Name")
    )'''

    tracks_table = '''CREATE TABLE IF NOT EXISTS "Tracks" (
	"Track_Name"	TEXT NOT NULL UNIQUE,
	"HRef"	TEXT NOT NULL,
	PRIMARY KEY("Track_Name")
    )'''

    laps_table = '''CREATE TABLE IF NOT EXISTS "Laps" (
	"Lap_Time"	REAL NOT NULL,
	"Driver"	TEXT NOT NULL,
	"PS_KG"	TEXT NOT NULL,
	"Track"	TEXT NOT NULL,
	"Vehicle"	TEXT NOT NULL,
	FOREIGN KEY("Track") REFERENCES "Tracks"("Track_Name"),
    FOREIGN KEY("Vehicle") REFERENCES "Vehicles"("Vehicle_Name")
    )'''

    try:
        c = conn.cursor()
        print("Creating vehicles table...")
        c.execute(vehicles_table)
        print("Creating tracks table...")
        c.execute(tracks_table)
        print("Creating laps table...")
        c.execute(laps_table)
        print("Table Created.")
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

    sql = ''' INSERT OR IGNORE INTO Tracks(Track_Name,HRef)
              VALUES(?,?) '''
              
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