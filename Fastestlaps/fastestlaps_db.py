# Fastestlaps database

import sqlite3
from sqlite3 import Error

LOGGING = "Logging sqlite db: "
PATH = "./scrap.db"

def create_database():
    # Create a connectio to db
    
    print(LOGGING + "Create " + PATH + "...")

    conn = None
    try:
        conn = sqlite3.connect(PATH)
        print("Version Database:" + sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def get_connection():
    # Create a database connection to the SQLite database specified by db_file
    # :param db_file: database file
    # :return: Connection object or None

    print(LOGGING + "Getting connection...")

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

    print(LOGGING + "Create Tables...")

    vehicles_table = '''CREATE TABLE IF NOT EXISTS "Vehicles" (
	"Vehicle_Name"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("Vehicle_Name")
    )'''

    tracks_table = '''CREATE TABLE IF NOT EXISTS "Tracks" (
	"Track_Name"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("Trak_Name")
    )'''

    laps_table = '''CREATE TABLE IF NOT EXISTS "Laps" (
	"Lap_ID"	INTEGER,
	"Time_Lap"	INTEGER NOT NULL,
	"Track"	TEXT NOT NULL,
	"Vehicle"	TEXT NOT NULL,
	FOREIGN KEY("Vehicle") REFERENCES "Vehicles"("Vehicle_Name"),
	FOREIGN KEY("Track") REFERENCES "Tracks"("Track_Name"),
	PRIMARY KEY("Lap_ID" AUTOINCREMENT)
    )'''

    try:
        c = conn.cursor()
        print(LOGGING + "Creating vehicles table...")
        c.execute(vehicles_table)
        print(LOGGING + "Creating tracks table...")
        c.execute(tracks_table)
        print(LOGGING + "Creating laps table...")
        c.exeute(laps_table)
        print("Table Created.")
    except Error as e:
        print(e)

def insert_new_lap(conn, lap):
    # Create a new lap into the laps table
    # :param conn: db connection.
    # :param lap: is a tuple.
    # :return: last row id.

    sql = ''' INSERT INTO Laps(Lap_Time,Track,Vehicle)
              VALUES(?,?,?) '''

    cur = conn.cursor()
    cur.execute(sql, lap)
    conn.commit()

    print("Insert: " + sql)
    return cur.lastrowid

def insert_new_tracks(conn, track):
    # Create a new lap into the laps table
    # :param conn: db connection.
    # :param track: is a tuple.
    # :return: last row id.

    sql = ''' INSERT INTO Tracks(Track_Name)
              VALUES(?) '''
              
    cur = conn.cursor()
    cur.execute(sql, track)
    conn.commit()

    print("Insert: " + sql)
    return cur.lastrowid

def insert_new_vehichle(conn, vehicle):
    # Create a new lap into the laps table
    # :param conn: db connection.
    # :param vehicle: is a tuple.
    # :return: last row id.

    sql = ''' INSERT INTO Vehicles(Vehicle_Name)
              VALUES(?) '''
              
    cur = conn.cursor()
    cur.execute(sql, vehicle)
    conn.commit()

    print("Insert: " + sql)
    return cur.lastrowid