# Fastestlaps database

import sqlite3
from sqlite3 import Error

PATH = "./scrap.db"

def extract_database(conn, min_vehicle_laps, min_track_laps):
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
    #             CREATE TEMP VIEW List_Motorcycles
    #             AS
    #             SELECT * FROM Specs
    #             WHERE Specs.Type = 'Motorcycle'
    #             '''
    # count_track = '''
    #             CREATE TEMP VIEW Track_Lap_Count
    #             AS
    #             SELECT
    #                 Laps.Track, COUNT(Laps.Vehicle)
    #             FROM
    #                 Laps INNER JOIN List_Cars ON Laps.Vehicle = List_Cars.Vehicle
    #             GROUP BY
    #                 Laps.Track
    #             ORDER BY
    #                 Laps.Track ASC
    #             '''
    # count_vehicle = '''
    #                 CREATE TEMP VIEW Vehicle_Lap_Count
    #                 AS
    #                 SELECT
    #                     List_Cars.Vehicle, COUNT(Laps.Track)
    #                 FROM
    #                     Laps INNER JOIN List_Cars ON Laps.Vehicle = List_Cars.Vehicle
    #                 GROUP BY
    #                     List_Cars.Vehicle
    #                 ORDER BY
    #                     List_Cars.Vehicle ASC
    #                 '''
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
        COUNT(Laps.Vehicle) >= {min_track_laps}
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
        Laps.Track ASC
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

def create_database():
    # Create a connection to db
    # :param:
    # :return: connection object or None.
    
    print("Version Database: " + sqlite3.version)
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
	"Lap_Time"	REAL NOT NULL,
	"Driver"	TEXT NOT NULL,
	"PS_KG"	TEXT NOT NULL,
	"Track"	TEXT NOT NULL,
	"Vehicle"	TEXT NOT NULL,
	FOREIGN KEY("Track") REFERENCES "Tracks"("Track_Name") ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY("Vehicle") REFERENCES "Vehicles"("Vehicle_Name") ON DELETE CASCADE ON UPDATE CASCADE
    )'''

    specs_table = '''CREATE TABLE IF NOT EXISTS "Specs" (
	"Vehicle"	        TEXT NOT NULL,
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

def insert_new_lap(conn, lap):
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

def insert_new_track(conn, track):
    # Create a new lap into the laps table
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

def insert_new_specs(conn, specs):
    # Create a new specs into the specs table
    # :param conn: db connection.
    # :param specs: is a tuple.
    # :return: last row id.

    sql = ''' INSERT OR IGNORE INTO Specs(Vehicle,Type,Type_Usage,Introduced_Year,Country,
    Curb_Weight,Wheelbase,Dim_Long,Dim_Wide,Dim_High,Zero_Hundred,Hundred_Zero,Top_Speed,
    Engine_Type,Displacement,Power_PS,Power_BHP,Power_KW,Torque,
    Power_Weight,Torque_Weight,Efficiency,Trasmission,Layout)
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''

    cur = conn.cursor()
    cur.execute(sql, specs)
    cur.close()
    conn.commit()

    print("Insert: " + str(specs))
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
    cur.close()
    conn.commit()

    print("Insert: " + str(vehicle))
    return cur.lastrowid

def insert_new_record(lap, track, vehicle):
    conn = get_connection()
    insert_new_vehichle(conn,vehicle)
    insert_new_track(conn,track)
    insert_new_lap(conn,lap)
    conn.close()

def get_all_laps(conn):
    # Get all laps from the laps table
    # :param conn: db connection.
    # :return: list of all record.
    
    print("Getting all laps data...")

    sql = ''' SELECT * FROM Laps '''
              
    cur = conn.cursor()
    cur.execute(sql)
    cur.close()

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
    cur.close()

    output = cur.fetchall()

    print("SELECT all tracks complete.")
    return output

def get_all_specs(conn):
    # Get all specs from the specs table
    # :param conn: db connection.
    # :return: list of all record.
    
    print("Getting all laps data...")

    sql = ''' SELECT * FROM Specs '''
              
    cur = conn.cursor()
    cur.execute(sql)
    cur.close()

    output = cur.fetchall()

    print("SELECT all laps complete.")
    return output

def get_all_vehicles(conn):
    # Get all vehicles from the vehicles table
    # :param conn: db connection.
    # :return: list of all record.

    print("Getting all vehicles data...")

    sql = ''' SELECT * FROM Vehicles '''
              
    cur = conn.cursor()
    cur.execute(sql)
    cur.close()

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
    cur.close()

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
    cur.close()

    output = cur.fetchall()

    print("SELECT specific track complete.")
    return output

def get_secific_stats(conn, vehicle_name):
    # Get specific stats from the stats table
    # :param conn: db connection.
    # :param vehicle_name: vehicle name string.
    # :return: list of all specific record.

    print("Getting " + vehicle_name +" vehicle data...")

    sql = ''' SELECT * FROM Specs WHERE Vehicle = ? '''
              
    cur = conn.cursor()
    cur.execute(sql, (vehicle_name, ))
    cur.close()

    output = cur.fetchall()

    print("SELECT specific vehicle complete.")
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
    cur.close()

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
    cur.close()
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
    cur.close()
    conn.commit()

    print("Delete: " + track_name)

def delete_specific_specs(conn, vehicle_name):
    # Delete a specs by vehicle name
    # :param conn: db connection.
    # :param vehicle_name: vehicle name string.
    # :return:
    
    sql = ''' DELETE FROM Specs WHERE Vehicle = ? '''
    cur = conn.cursor()
    cur.execute(sql, (vehicle_name,))
    cur.close()
    conn.commit()

    print("Delete: " + vehicle_name)

def delete_specific_vehicle(conn, vehicle_name):
    # Delete a vehicle by vehicle name
    # :param conn: db connection.
    # :param vehicle_name: vehicle name string.
    # :return:
    
    sql = ''' DELETE FROM Vehicles WHERE Vehicles_Name = ? '''
    cur = conn.cursor()
    cur.execute(sql, (vehicle_name,))
    cur.close()
    conn.commit()

    print("Delete: " + vehicle_name)

def update_specific_lap(conn, track_name, vehicle_name, values):
    # Update a vehicle by track name and vehicle name
    # :param conn: db connection.
    # :param track_name: track name string.
    # :param vehicle_name: vehicle name string.
    # :return: number of updatetd row.

    raise NotImplementedError
    
def update_specific_track(conn, track_name, values):
    # Update a vehicle by track name
    # :param conn: db connection.
    # :param vehicle_name: vehicle name string.
    # :return: number of updatetd row.

    raise NotImplementedError

def update_specific_specs(conn, vehicle_name, values):
    # Update a specs by vehicle name
    # :param conn: db connection.
    # :param vehicle_name: vehicle name string.
    # :return: number of updatetd row.

    raise NotImplementedError

def update_specific_vehicle(conn, vehicle_name, values):
    # Update a vehicle by vehicle name
    # :param conn: db connection.
    # :param vehicle_name: vehicle name string.
    # :return: number of updatetd row.

    raise NotImplementedError
