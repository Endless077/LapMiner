#  ______       _    _________    _      ______       _      ______  ________  
# |_   _ `.    / \  |  _   _  |  / \    |_   _ \     / \   .' ____ \|_   __  | 
#   | | `. \  / _ \ |_/ | | \_| / _ \     | |_) |   / _ \  | (___ \_| | |_ \_| 
#   | |  | | / ___ \    | |    / ___ \    |  __'.  / ___ \  _.____`.  |  _| _  
#  _| |_.' _/ /   \ \_ _| |_ _/ /   \ \_ _| |__) _/ /   \ \| \____) |_| |__/ | 
# |______.|____| |____|_____|____| |____|_______|____| |____\______.|________|

import re
import sqlite3
from sqlite3 import Error

import classes
import utils

PATH = "../Lap-Time-Prediction/Generator/database/database.db"

def upgrade(dump_database_path: str):
    # Upgrade function from dump.db to database.db (see ./class_diagram)
    # :param dump_database_path: a string path of dump.db.
    # :return:
    
    utils.create_SQLite_database(PATH)

    conn_new_db = utils.get_SQLite_connection(PATH)
    conn_old_db = utils.get_SQLite_connection(dump_database_path)

    create_tables(conn_new_db)

   
    laps_track =    ''' SELECT Lap_Time, Driver, Track, Vehicle FROM Laps WHERE Laps.Track = ? '''
    specs_vehicle = ''' SELECT Specs.* FROM Specs WHERE Specs.Vehicle = ? '''  
 
    all_tracks =    ''' SELECT Track_Name, Country, Total_Length FROM Tracks '''
    all_vehicles =  ''' SELECT Vehicle_Name,HRef FROM Vehicles '''  
    
    cur_new = conn_new_db.cursor()
    cur_old = conn_old_db.cursor()

    cur_old.execute(all_vehicles)
    
    vehicles = cur_old.fetchall()
    for vehicle in vehicles:
        new_vehicle = adapt_vehicle((-1,vehicle[0],None), True)
        if vehicle[1] is not None:
            new_vehicle = adapt_vehicle(cur_old.execute(specs_vehicle,(vehicle[0],)).fetchone(), False)
        insert_new_vehicle(conn_new_db, new_vehicle)
        print("######################")
    
    cur_old.execute(all_tracks)

    tracks = cur_old.fetchall()
    for track in tracks:
        new_track = adapt_track(track)
        
        curr_track = new_track
        curr_track.track_id = insert_new_track(conn_new_db,new_track)
        curr_laps = cur_old.execute(laps_track, (new_track.track_name,)).fetchall()
        
        for lap in curr_laps:
            curr_vehicle = adapt_vehicle(cur_new.execute('SELECT * FROM Vehicles WHERE Vehicle_Name = ?',(lap[3],)).fetchone(), True)
            new_lap = adapt_lap((*lap[0:2],curr_track,curr_vehicle))
            insert_new_lap(conn_new_db,new_lap)
        print("######################")
    cur_new.close()
    cur_old.close()

def adapt_lap(lap_record: tuple):
    # Adapt a laps dump.db record to Laps object class
    # :param lap_record: a tuple.
    # :return:
    return classes.LapTime(-1,*lap_record)

def adapt_track(track_record: tuple):
    # Adapt a tracks dump.db record to Tracks object class
    # :param track_record: a tuple.
    # :return:
    return classes.Track(-1,*track_record)

def adapt_vehicle(vehicle_record: tuple, no_specs: bool):
    # Adapt a dump.db record to Vehicle object class
    # :param vehicle_record: a tuple.
    # :param no_specs: a boolean (if true return vehicle without specs object)
    # :return:
    
    if no_specs:
        layout = classes.Layout(-1,None,None,None)
        dimensions = classes.Dimensions(-1,None,None,None,None,None)
        engine = classes.Engine(-1,None,None,None,None)
        trasmission = classes.Trasmission(-1,None,None,None)
        performance = classes.Performance(-1,None,None,None)
        overview = classes.Overview(-1,None,None,None)
        return classes.Vehicle(*vehicle_record,layout,dimensions,engine,trasmission,performance,overview)
    
    get_layout = [None, None]
    if vehicle_record[24] is not None:
        get_layout = [string.strip().split(" ")[0].title() for string in vehicle_record[24].split(",")]
    layout = classes.Layout(-1,*get_layout[0:2],vehicle_record[3])

    dimensions = classes.Dimensions(-1,*vehicle_record[6:11])    
    engine = classes.Engine(-1,*vehicle_record[14:17],vehicle_record[19])
    
    get_trasmission = [vehicle_record[23],"Other",None]
    if vehicle_record[23] is not None:
        if re.search(" or ", vehicle_record[23].lower()):
            get_trasmission[0] = "unknown"
        else:
            type_list = ["manual", "automatic", "semi-automatic", "semi automatic", "dual-clutch", "dual clutch", "sequential"]
            type_index = [int(vehicle_record[23].lower().find(type_value)) for type_value in type_list]
            occurrences = [value for value in type_index if value > 0]
            if(len(occurrences) > 0):
                get_trasmission[1] = type_list[type_index.index(min(occurrences))].replace(" ","-").title()
    
            n_trasmission = re.search(r'\d+', vehicle_record[23])
            if n_trasmission is not None:
                get_trasmission[2] = n_trasmission.group()
        
    trasmission = classes.Trasmission(-1,*get_trasmission[0:3])

    performance = classes.Performance(-1,*vehicle_record[11:14])
    overview = classes.Overview(-1,vehicle_record[1],vehicle_record[5],vehicle_record[4])
    
    return classes.Vehicle(-1,vehicle_record[0],vehicle_record[2],layout,dimensions,engine,trasmission,performance,overview)

def create_tables(conn: sqlite3.Connection):
    # Create all tables of database
    # :param conn: db connection.
    # :return:

    print("Creating Tables...")

    vehicles_table = ''' CREATE TABLE IF NOT EXISTS "Vehicles" (
	"Vehicle_ID"	INTEGER,
	"Vehicle_Name"	TEXT UNIQUE,
	"Type"	        TEXT CHECK("Type" IN ('Car', 'Motorcycle')),
	PRIMARY KEY("Vehicle_ID" AUTOINCREMENT)
    ) '''

    tracks_table = ''' CREATE TABLE IF NOT EXISTS "Tracks" (
	"Track_ID"	    INTEGER,
	"Track_Name"	TEXT UNIQUE,
	"Country"	    TEXT,
	"Total_Length"	REAL,
	PRIMARY KEY("Track_ID" AUTOINCREMENT)
    ) '''

    layout_table = ''' CREATE TABLE IF NOT EXISTS "Layout" (
	"Layout_ID"	    INTEGER,
	"Engine_Layout"	TEXT CHECK(Engine_Layout IN ('Front','Rear','Middle')),
	"Wheel_Drive"	TEXT CHECK(Wheel_Drive IN ('Front','Rear','All')),
	"Class_Type"	TEXT,
	"Vehicle_ID"	INTEGER,
	FOREIGN KEY("Vehicle_ID") REFERENCES "Vehicles"("Vehicle_ID") ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY("Layout_ID" AUTOINCREMENT)
    ) '''

    dimensions_table = ''' CREATE TABLE IF NOT EXISTS "Dimensions" (
	"Dimensions_ID"	INTEGER,
	"Curb_Weight"	REAL,
	"Wheelbase"	    REAL,
	"Long"	        REAL,
	"High"	        REAL,
	"Wide"	        REAL,
	"Vehicle_ID"	INTEGER,
	PRIMARY KEY("Dimensions_ID" AUTOINCREMENT),
	FOREIGN KEY("Vehicle_ID") REFERENCES "Vehicles"("Vehicle_ID") ON DELETE CASCADE ON UPDATE CASCADE
    ) '''

    engine_table = ''' CREATE TABLE IF NOT EXISTS "Engine" (
	"Engine_ID"	    INTEGER,
	"Engine"	    TEXT,
	"Displacement"	REAL,
	"Power"	        INTEGER,
	"Torque"	    INTEGER,
	"Vehicle_ID"	INTEGER,
	PRIMARY KEY("Engine_ID" AUTOINCREMENT),
	FOREIGN KEY("Vehicle_ID") REFERENCES "Vehicles"("Vehicle_ID") ON DELETE CASCADE ON UPDATE CASCADE
    ) '''
    
    trasmission_table = ''' CREATE TABLE IF NOT EXISTS "Trasmission" (
	"Trasmission_ID"	INTEGER,
	"Trasmission_Name"	TEXT,
	"Trasmission_Type"	TEXT CHECK(Trasmission_Type IN ('Manual', 'Automatic', 'Semi-Automatic', 'Dual-Clutch', 'Sequential', 'Other')),
	"N_Trasmission"	    INTEGER,
	"Vehicle_ID"	    INTEGER,
    PRIMARY KEY("Trasmission_ID" AUTOINCREMENT),
	FOREIGN KEY("Vehicle_ID") REFERENCES "Vehicles"("Vehicle_ID") ON DELETE CASCADE ON UPDATE CASCADE
    ) '''
    
    performance_table = ''' CREATE TABLE IF NOT EXISTS "Performance" (
	"Perofrmance_ID"	INTEGER,
	"Zero_Hundred"	    REAL,
	"Break_Distance"	REAL,
	"Top_Speed"	        REAL,
	"Vehicle_ID"	    INTEGER,
	PRIMARY KEY("Perofrmance_ID" AUTOINCREMENT),
	FOREIGN KEY("Vehicle_ID") REFERENCES "Vehicles"("Vehicle_ID") ON DELETE CASCADE ON UPDATE CASCADE
    ) '''
    
    overview_table = ''' CREATE TABLE IF NOT EXISTS "Overview" (
	"Overview_ID"	    INTEGER,
	"Manufacturer"	    TEXT,
	"Origin_Country"	TEXT,
	"Introduced_Year"	INTEGER,
	"Vehicle_ID"	    INTEGER,
    PRIMARY KEY("Overview_ID" AUTOINCREMENT),
	FOREIGN KEY("Vehicle_ID") REFERENCES "Vehicles"("Vehicle_ID") ON DELETE CASCADE ON UPDATE CASCADE
    ) '''
    
    laps_table = ''' CREATE TABLE IF NOT EXISTS "Laps" (
	"Lap_Time_ID"	INTEGER,
	"Lap_Time"	    REAL,
	"Driver"	    TEXT,
	"Track_ID"	    INTEGER,
	"Vehicle_ID"	INTEGER,
    PRIMARY KEY("Lap_Time_ID" AUTOINCREMENT),
	FOREIGN KEY("Track_ID") REFERENCES "Tracks"("Track_ID") ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY("Vehicle_ID") REFERENCES "Vehicles"("Vehicle_ID") ON DELETE CASCADE ON UPDATE CASCADE
    ) '''

    try:
        cur = conn.cursor()
        print("Creating vehicles table...")
        cur.execute(vehicles_table)
        print("Creating tracks table...")
        cur.execute(tracks_table)
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
        print("Creating laps table...")
        cur.execute(laps_table)
        cur.close()

        conn.commit()
        print("Tables created.")
    except Error as e:
        print(e)

def create_views(conn: sqlite3.Connection, min_track_laps: int, min_vehicle_laps: int):
    # Create a table from the create_table_sql statement
    # :param conn: db connection.
    # :return:

    print("Creating Views...")

    cars = '''
    CREATE TEMP VIEW List_Cars
    AS
    SELECT * FROM Vehicles
    WHERE Vehicles.Type = 'Car'
    '''

    # motorcycle = '''
    # CREATE TEMP VIEW List_Motorcycles
    # AS
    # SELECT * FROM Vehicles
    # WHERE Vehicles.Type = 'Motorcycle'
    # '''

    extract_vehicle = f'''
    CREATE TEMP VIEW Extract_Vehicles_List
    AS
    SELECT
        List_Cars.*
    FROM
        Laps JOIN List_Cars ON Laps.Vehicle_ID = List_Cars.Vehicle_ID
        JOIN Tracks ON Laps.Track_ID = Tracks.Track_ID
    GROUP BY
        Laps.Vehicle_ID
    HAVING
        COUNT(Laps.Track_ID) >= {min_vehicle_laps}
    ORDER BY
        List_Cars.Vehicle_Name ASC
    '''

    export_vehicle = '''
    CREATE TEMP VIEW Export_Vehicles_List
    AS
    SELECT 
        EVL.Vehicle_Name,EVL.Type,
        Overview.Manufacturer,Overview.Origin_Country,Overview.Introduced_Year,
        Performance.Zero_Hundred,Performance.Break_Distance,Performance.Top_Speed,
        Dimensions.Curb_Weight,Dimensions.Wheelbase,Dimensions.Long,Dimensions.High,Dimensions.Wide,
        Engine.Engine,Engine.Displacement,Engine.Power,Engine.Torque,
        Layout.Engine_Layout,Layout.Wheel_Drive,Layout.Class_Type,
        Trasmission.Trasmission_Name,Trasmission.Trasmission_Type,Trasmission.N_Trasmission
    FROM Extract_Vehicles_List AS EVL
        JOIN Layout ON EVL.Vehicle_ID = Layout.Vehicle_ID
        JOIN Dimensions ON EVL.Vehicle_ID = Dimensions.Vehicle_ID
        JOIN Engine ON EVL.Vehicle_ID = Engine.Vehicle_ID
        JOIN Trasmission ON EVL.Vehicle_ID = Trasmission.Vehicle_ID
        JOIN Performance ON EVL.Vehicle_ID = Performance.Vehicle_ID
        JOIN Overview ON EVL.Vehicle_ID = Overview.Vehicle_ID
    ORDER BY
        EVL.Vehicle_Name ASC
    '''
    
    extract_track = f'''
    CREATE TEMP VIEW Extract_Tracks_List
    AS
    SELECT
        Tracks.*
    FROM
        Laps JOIN List_Cars ON Laps.Vehicle_ID = List_Cars.Vehicle_ID
        JOIN Tracks ON Laps.Track_ID = Tracks.Track_ID
    GROUP BY
        Laps.Track_ID
    HAVING
        COUNT(DISTINCT Laps.Vehicle_ID) >= {min_track_laps}
    ORDER BY
        Tracks.Track_Name ASC
    '''
    
    export_track = f'''
    CREATE TEMP VIEW Export_Tracks_List
    AS
    SELECT 
	    ETL.Track_Name,ETL.Country,ETL.Total_Length
    FROM 
        Extract_Tracks_List AS ETL
    ORDER BY
        ETL.Track_Name ASC
    '''

    extract_laps = '''
    CREATE TEMP VIEW Extract_Laps_List
    AS
    SELECT
        Laps.*
    FROM
        Laps JOIN Extract_Vehicles_List AS EVL ON Laps.Vehicle_ID = EVL.Vehicle_ID
        JOIN Extract_Tracks_List AS ETL ON Laps.Track_ID = ETL.Track_ID
    ORDER BY
        Track_Name ASC
    '''

    export_laps = '''
    CREATE TEMP VIEW Export_Laps_List
    AS
    SELECT 
	    ELL.Lap_Time,ELL.Driver,Tracks.Track_Name,List_Cars.Vehicle_Name
    FROM 
	    Extract_Laps_List AS ELL JOIN Tracks ON ELL.Track_ID = Tracks.Track_ID
	    JOIN List_Cars ON ELL.Vehicle_ID = List_Cars.Vehicle_ID
    ORDER BY
	    Tracks.Track_Name ASC
    '''
    
    try:
        cur = conn.cursor()
        print("Creating List Cars view...")
        cur.execute(cars)
        # print("Creating List Motorcycles view...")
        # c.execute(motorcycle)
        print("Creating Merge Vehicle List view...")
        cur.execute(extract_vehicle)
        print("Creating Merge Track List view...")
        cur.execute(extract_track)
        print("Creating Merge Lap List view...")
        cur.execute(extract_laps)
        print("Creating Export Vehicle List view...")
        cur.execute(export_vehicle)
        print("Creating Export Track List view...")
        cur.execute(export_track)
        print("Creating Export Lap List view...")
        cur.execute(export_laps)
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

def insert_new_vehicle(conn: sqlite3.Connection, vehicle: classes.Vehicle):
    # Create a new vehicle into the vehicles table and all components
    # :param conn: db connection.
    # :param car: is a car object.
    # :return: last row id.

    sql = ''' INSERT OR IGNORE INTO Vehicles(Vehicle_Name,Type)
              VALUES(?,?) '''
    
    insert_tuple = (vehicle.vehicle_name, vehicle.type) 

    cur = conn.cursor()
    cur.execute(sql, insert_tuple)

    curr_id = cur.lastrowid
    
    insert_Layout(conn, curr_id, vehicle.layout)
    insert_dimensions(conn, curr_id, vehicle.dimensions)
    insert_engine(conn, curr_id, vehicle.engine)
    insert_trasmission(conn, curr_id, vehicle.trasmission)
    insert_performance(conn, curr_id, vehicle.performance)
    insert_overview(conn, curr_id, vehicle.overview)

    cur.close()

    conn.commit()

    print("Insert: " + str(insert_tuple))
    return cur.lastrowid

def insert_Layout(conn: sqlite3.Connection, vehicle_id: int, layout: classes.Layout):
    # Create a new layout ref into the layout table
    # :param conn: db connection.
    # :param vehicle_id: id of ref vehicle.
    # :param layout: a layout object.
    # :return: last row id.

    sql = ''' INSERT OR IGNORE INTO Layout(Engine_Layout,Wheel_Drive,Class_Type,Vehicle_ID)
              VALUES(?,?,?,?) '''
    
    insert_tuple = (layout.engine_layout, layout.wheel_drive, layout.class_type, vehicle_id) 

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

    sql = ''' INSERT INTO Trasmission(Trasmission_Name,Trasmission_Type,N_Trasmission,Vehicle_ID)
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
    # Get specific laptime from the laps table
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
    # Get specific track from the tracks table
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
    # Get specific vehicle from the vehicles table join all specs
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
    # Delete a track by track name OR track id
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
    # Delete a vehicle by vehicle name OR vehicle id
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
    # Update a lap by track name and vehicle name
    # :param conn: db connection.
    # :param track_id: track id.
    # :param vehicle_id: vehicle id.
    # :return: number of updatetd row.

    raise NotImplementedError
    
def update_specific_track(conn: sqlite3.Connection, track_id: int, track_name: str, values: tuple):
    # Update a track by track name
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
