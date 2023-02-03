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

PATH = "../Lap-Time-Prediction/generator/database/database.db"

def upgrade(dump_database_path: str):
    # Upgrade function from dump.db to database.db (see ./class_diagram)
    # :param dump_database_path: a string path of dump.db.
    # :return:
    
    utils.create_SQLite_database(PATH)

    conn_new_db = utils.get_SQLite_connection(PATH)
    conn_old_db = utils.get_SQLite_connection(dump_database_path)

    create_tables(conn_new_db)

   
    laps_track =    ''' SELECT lap_time, driver, track, vehicle FROM LAPS WHERE LAPS.track = ? '''
    specs_vehicle = ''' SELECT * FROM SPECS WHERE SPECS.Vehicle = ? '''  
 
    all_tracks =    ''' SELECT track_name, country, total_length FROM TRACKS '''
    all_vehicles =  ''' SELECT * FROM VEHICLES '''  
    
    cur_new = conn_new_db.cursor()
    cur_old = conn_old_db.cursor()
    
    print("######################")
    vehicles = cur_old.execute(all_vehicles).fetchall()
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
            curr_vehicle = adapt_vehicle(cur_new.execute('SELECT * FROM VEHICLES WHERE vehicle_name = ?',(lap[3],)).fetchone(), True)
            new_lap = adapt_lap((*lap[0:2],curr_track,curr_vehicle))
            insert_new_lap(conn_new_db,new_lap)
        print("######################")
    cur_new.close()
    cur_old.close()

def adapt_lap(lap_record: tuple):
    # Adapt a laps dump.db record to LAPS object class
    # :param lap_record: a tuple.
    # :return:
    return classes.LapTime(-1,*lap_record)

def adapt_track(track_record: tuple):
    # Adapt a tracks dump.db record to TRACKS object class
    # :param track_record: a tuple.
    # :return:
    return classes.Track(-1,*track_record)

def adapt_vehicle(vehicle_record: tuple, no_specs: bool):
    # Adapt a dump.db record to Vehicle object class
    # :param vehicle_record: a tuple.
    # :param no_specs: a boolean (if true return vehicle without specs object)
    # :return:
    
    # DUMP DB STRUCT:
        # [0] "vehicle"	            TEXT NOT NULL   - Vehicle
        # [1] "manufacturer"        TEXT            - Overview
        # [2] "model"               TEXT            - Overview
        # [3] "type"	            TEXT            - Vehicle
        # [4] "type_usage"	        TEXT            - Layout  
        # [5] "introduced_year"     INTEGER         - Overview
        # [6] "country"	            TEXT            - Overview      
        # [7] "curb_weight"	        REAL            - Dimensions
        # [8] "wheelbase"	        REAL            - Dimensions
        # [9] "dim_long"	        REAL            - Dimensions
        # [10] "dim_wide"	        REAL            - Dimensions
        # [11] "dim_high"	        REAL            - Dimensions
        # [12] "zero_hundred"	    REAL            - Performance
        # [13] "hundred_zero"	    REAL            - Performance
        # [14] "top_speed"	        INTEGER         - Performance
        # [15] "engine_type"	    TEXT            - Engine
        # [16] "displacement"	    REAL            - Engine
        # [17] "power_ps"	        INTEGER         - Engine
        # [18] "power_bhp"	        INTEGER         - Engine (ignore)
        # [19] "power_kw"	        INTEGER         - Engine (ignore)
        # [20] "torque"	            INTEGER         - Engine
        # [21] "power_weight"	    INTEGER         - Engine (ignore)
        # [22] "torque_weight"	    INTEGER         - Engine (ignore)
        # [23] "efficiency"	        INTEGER         - Engine (ignore)
        # [24] "trasmission"	    TEXT            - Trasmission
        # [25] "layout"	            TEXT            - Layout

    if no_specs:
        layout = classes.Layout(-1,None,None,None)
        dimensions = classes.Dimensions(-1,None,None,None,None,None)
        engine = classes.Engine(-1,None,None,None,None)
        trasmission = classes.Trasmission(-1,None,None,None)
        performance = classes.Performance(-1,None,None,None)
        overview = classes.Overview(-1,None,None,None,None)
        return classes.Vehicle(*vehicle_record,layout,dimensions,engine,trasmission,performance,overview)

    get_layout = [None, None]
    if vehicle_record[25] is not None:
        get_layout = [string.strip().split(" ")[0].title() for string in vehicle_record[25].split(",")]
    layout = classes.Layout(-1,*get_layout[0:2],vehicle_record[4])

    dimensions = classes.Dimensions(-1,*vehicle_record[7:12])    
    engine = classes.Engine(-1,*vehicle_record[15:18],vehicle_record[20])
    
    get_trasmission = [vehicle_record[24],"Other",None]
    if vehicle_record[24] is not None:
        if re.search(r" or |\/", vehicle_record[24].lower()):
            get_trasmission[0] = "Other"
        else:
            type_list = ["manual", "automatic", "semi-automatic", "semi automatic", "dual-clutch", "dual clutch", "sequential"]
            type_index = [int(vehicle_record[24].lower().find(type_value)) for type_value in type_list]
            occurrences = [value for value in type_index if value > 0]
            if(len(occurrences) > 0):
                get_trasmission[1] = type_list[type_index.index(min(occurrences))].replace(" ","-").title()

            number = None
            if(str(vehicle_record[24][0]).isnumeric()):
                n_trasmission = re.search(r'\d+', vehicle_record[24])
                if(n_trasmission is not None):
                    number = n_trasmission.group()
            else:
                n_trasmission = re.findall(r'\d+', vehicle_record[24])
                if(len(n_trasmission) > 0):
                    number = min([int(i) for i in n_trasmission])
                            
            get_trasmission[2] = number
        
    trasmission = classes.Trasmission(-1,*get_trasmission[0:3])

    performance = classes.Performance(-1,*vehicle_record[12:15])
    overview = classes.Overview(-1,*vehicle_record[1:3],vehicle_record[6],vehicle_record[5])
    
    return classes.Vehicle(-1,vehicle_record[0],vehicle_record[3],layout,dimensions,engine,trasmission,performance,overview)

def create_tables(conn: sqlite3.Connection):
    # Create all tables of database
    # :param conn: db connection.
    # :return:

    print("Creating Tables...")

    vehicles_table = ''' CREATE TABLE IF NOT EXISTS "VEHICLES" (
	"vehicle_id"	INTEGER,
	"vehicle_name"	TEXT UNIQUE,
	"type"	        TEXT CHECK("type" IN ('Car', 'Motorcycle')),
	PRIMARY KEY("vehicle_id" AUTOINCREMENT)
    ) '''

    tracks_table = ''' CREATE TABLE IF NOT EXISTS "TRACKS" (
	"track_id"	    INTEGER,
	"track_name"	TEXT UNIQUE,
	"country"	    TEXT,
	"total_length"	REAL,
	PRIMARY KEY("track_id" AUTOINCREMENT)
    ) '''

    layout_table = ''' CREATE TABLE IF NOT EXISTS "LAYOUT" (
	"layout_id"	    INTEGER,
	"engine_layout"	TEXT CHECK(engine_layout IN ('Front','Rear','Middle')),
	"wheel_drive"	TEXT CHECK(wheel_drive IN ('Front','Rear','All')),
	"class_type"	TEXT,
	"vehicle_id"	INTEGER,
	FOREIGN KEY("vehicle_id") REFERENCES "VEHICLES"("vehicle_id") ON DELETE CASCADE ON UPDATE CASCADE,
	PRIMARY KEY("layout_id" AUTOINCREMENT)
    ) '''

    dimensions_table = ''' CREATE TABLE IF NOT EXISTS "DIMENSIONS" (
	"dimensions_id"	INTEGER,
	"curb_weight"	REAL,
	"wheelbase"	    REAL,
	"long"	        REAL,
	"wide"	        REAL,
    "high"	        REAL,
	"vehicle_id"	INTEGER,
	PRIMARY KEY("dimensions_id" AUTOINCREMENT),
	FOREIGN KEY("vehicle_id") REFERENCES "VEHICLES"("vehicle_id") ON DELETE CASCADE ON UPDATE CASCADE
    ) '''

    engine_table = ''' CREATE TABLE IF NOT EXISTS "ENGINE" (
	"engine_id"	    INTEGER,
	"engine_name"	TEXT,
	"displacement"	REAL,
	"power"	        INTEGER,
	"torque"	    INTEGER,
	"vehicle_id"	INTEGER,
	PRIMARY KEY("engine_id" AUTOINCREMENT),
	FOREIGN KEY("vehicle_id") REFERENCES "VEHICLES"("vehicle_id") ON DELETE CASCADE ON UPDATE CASCADE
    ) '''
    
    trasmission_table = ''' CREATE TABLE IF NOT EXISTS "TRASMISSION" (
	"trasmission_id"	INTEGER,
	"trasmission_name"	TEXT,
	"trasmission_type"	TEXT CHECK(trasmission_type IN ('Manual', 'Automatic', 'Semi-Automatic', 'Dual-Clutch', 'Sequential', 'Other')),
	"n_trasmission"	    INTEGER,
	"vehicle_id"	    INTEGER,
    PRIMARY KEY("trasmission_id" AUTOINCREMENT),
	FOREIGN KEY("vehicle_id") REFERENCES "VEHICLES"("vehicle_id") ON DELETE CASCADE ON UPDATE CASCADE
    ) '''
    
    performance_table = ''' CREATE TABLE IF NOT EXISTS "PERFORMANCE" (
	"perofrmance_id"	INTEGER,
	"accelleration"	    REAL,
	"break_distance"	REAL,
	"top_speed"	        REAL,
	"vehicle_id"	    INTEGER,
	PRIMARY KEY("perofrmance_id" AUTOINCREMENT),
	FOREIGN KEY("vehicle_id") REFERENCES "VEHICLES"("vehicle_id") ON DELETE CASCADE ON UPDATE CASCADE
    ) '''
    
    overview_table = ''' CREATE TABLE IF NOT EXISTS "OVERVIEW" (
	"overview_id"	    INTEGER,
	"manufacturer"	    TEXT,
    "model"             TEXT,
	"origin_country"	TEXT,
	"introduced_year"	INTEGER,
	"vehicle_id"	    INTEGER,
    PRIMARY KEY("overview_id" AUTOINCREMENT),
	FOREIGN KEY("vehicle_id") REFERENCES "VEHICLES"("vehicle_id") ON DELETE CASCADE ON UPDATE CASCADE
    ) '''
    
    laps_table = ''' CREATE TABLE IF NOT EXISTS "LAPS" (
	"lap_time_id"	INTEGER,
	"lap_time"	    REAL,
	"driver"	    TEXT,
	"track_id"	    INTEGER,
	"vehicle_id"	INTEGER,
    PRIMARY KEY("lap_time_id" AUTOINCREMENT),
	FOREIGN KEY("track_id") REFERENCES "TRACKS"("track_id") ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY("vehicle_id") REFERENCES "VEHICLES"("vehicle_id") ON DELETE CASCADE ON UPDATE CASCADE
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
    CREATE TEMP VIEW CARS
    AS
    SELECT * FROM VEHICLES
    WHERE VEHICLES.type = 'Car'
    '''

    # motorcycle = '''
    # CREATE TEMP VIEW MOTORCYCLES
    # AS
    # SELECT * FROM VEHICLES
    # WHERE VEHICLES.type = 'Motorcycle'
    # '''

    extract_vehicle = f'''
    CREATE TEMP VIEW EXTRACT_VEHICLES_LIST
    AS
    SELECT
        CARS.*
    FROM
        LAPS JOIN CARS ON LAPS.vehicle_id = CARS.vehicle_id
        JOIN TRACKS ON LAPS.track_id = TRACKS.track_id
    GROUP BY
        LAPS.vehicle_id
    HAVING
        COUNT(LAPS.track_id) >= {min_vehicle_laps}
    ORDER BY
        CARS.vehicle_name ASC
    '''

    export_vehicle = '''
    CREATE TEMP VIEW EXPORT_VEHICLES_LIST
    AS
    SELECT 
        EVL.vehicle_name,EVL.type,
        OVERVIEW.manufacturer,OVERVIEW.model,OVERVIEW.origin_country,OVERVIEW.introduced_year,
        PERFORMANCE.accelleration,PERFORMANCE.break_distance,PERFORMANCE.top_speed,
        DIMENSIONS.curb_weight,DIMENSIONS.wheelbase,DIMENSIONS.long,DIMENSIONS.wide,DIMENSIONS.high,
        ENGINE.engine_name,ENGINE.displacement,ENGINE.power,ENGINE.torque,
        LAYOUT.engine_layout,LAYOUT.wheel_drive,LAYOUT.class_type,
        TRASMISSION.trasmission_name,TRASMISSION.trasmission_type,TRASMISSION.n_trasmission
    FROM EXTRACT_VEHICLES_LIST AS EVL
        JOIN LAYOUT ON EVL.vehicle_id = LAYOUT.vehicle_id
        JOIN DIMENSIONS ON EVL.vehicle_id = DIMENSIONS.vehicle_id
        JOIN ENGINE ON EVL.vehicle_id = ENGINE.vehicle_id
        JOIN TRASMISSION ON EVL.vehicle_id = TRASMISSION.vehicle_id
        JOIN PERFORMANCE ON EVL.vehicle_id = PERFORMANCE.vehicle_id
        JOIN OVERVIEW ON EVL.vehicle_id = OVERVIEW.vehicle_id
    ORDER BY
        EVL.vehicle_name ASC
    '''
    
    extract_track = f'''
    CREATE TEMP VIEW EXTRACT_TRACKS_LIST
    AS
    SELECT
        TRACKS.*
    FROM
        LAPS JOIN CARS ON LAPS.vehicle_id = CARS.vehicle_id
        JOIN TRACKS ON LAPS.track_id = TRACKS.track_id
    GROUP BY
        LAPS.track_id
    HAVING
        COUNT(DISTINCT LAPS.vehicle_id) >= {min_track_laps}
    ORDER BY
        TRACKS.track_name ASC
    '''
    
    export_track = f'''
    CREATE TEMP VIEW EXPORT_TRACKS_LIST
    AS
    SELECT 
	    ETL.track_name,ETL.country,ETL.total_length
    FROM 
        EXTRACT_TRACKS_LIST AS ETL
    ORDER BY
        ETL.track_name ASC
    '''

    extract_laps = '''
    CREATE TEMP VIEW EXTRACT_LAPS_LIST
    AS
    SELECT
        LAPS.*
    FROM
        LAPS JOIN EXTRACT_VEHICLES_LIST AS EVL ON LAPS.vehicle_id = EVL.vehicle_id
        JOIN EXTRACT_TRACKS_LIST AS ETL ON LAPS.track_id = ETL.track_id
    ORDER BY
        track_name ASC
    '''

    export_laps = '''
    CREATE TEMP VIEW EXPORT_LAPS_LIST
    AS
    SELECT 
	    ELL.lap_time,ELL.driver,TRACKS.track_name,CARS.vehicle_name
    FROM 
	    EXTRACT_LAPS_LIST AS ELL JOIN TRACKS ON ELL.track_id = TRACKS.track_id
	    JOIN CARS ON ELL.vehicle_id = CARS.vehicle_id
    ORDER BY
	    TRACKS.track_name ASC
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

    del1 = ''' DELETE FROM LAPS '''
    del2 = ''' DELETE FROM TRACKS '''
    del3 = ''' DELETE FROM VEHICLES '''

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

    sql = ''' INSERT OR IGNORE INTO LAPS(lap_time,driver,track_id,vehicle_id)
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

    sql = ''' INSERT OR IGNORE INTO TRACKS(track_name,country,total_length)
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

    sql = ''' INSERT OR IGNORE INTO VEHICLES(vehicle_name,type)
              VALUES(?,?) '''
    
    insert_tuple = (vehicle.vehicle_name, vehicle.vehicle_type) 

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

    sql = ''' INSERT OR IGNORE INTO LAYOUT(engine_layout,wheel_drive,class_type,vehicle_id)
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

    sql = ''' INSERT OR IGNORE INTO DIMENSIONS(curb_weight,wheelbase,long,wide,high,vehicle_id)
              VALUES(?,?,?,?,?,?) '''
    
    insert_tuple = (dimensions.curb_weight, dimensions.wheelbase, dimensions.long, dimensions.wide, dimensions.high, vehicle_id) 

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

    sql = ''' INSERT OR IGNORE INTO ENGINE(engine_name,displacement,power,torque,vehicle_id)
              VALUES(?,?,?,?,?) '''
    
    insert_tuple = (engine.engine_name, engine.displacement, engine.power, engine.torque, vehicle_id)

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

    sql = ''' INSERT INTO TRASMISSION(trasmission_name,trasmission_type,n_trasmission,vehicle_id)
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

    sql = ''' INSERT OR IGNORE INTO PERFORMANCE(accelleration,break_distance,top_speed,vehicle_id)
              VALUES(?,?,?,?) '''
    
    insert_tuple = (performance.accelleration, performance.break_distance, performance.top_speed, vehicle_id) 

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

    sql = ''' INSERT OR IGNORE INTO OVERVIEW(manufacturer,model,origin_country,introduced_year,vehicle_id)
              VALUES(?,?,?,?,?) '''
    
    insert_tuple = (overview.manufacturer, overview.model, overview.origin_country, overview.introduced_year, vehicle_id) 

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

def get_all_vehicles_specs(conn: sqlite3.Connection):
    # Get all vehicles from the vehicles table join all specs
    # :param conn: db connection.
    # :return: list of all record.

    print("Getting all vehicles data...")

    sql = ''' SELECT * FROM VEHICLES 
            JOIN LAYOUT ON VEHICLES.vehicle_id = LAYOUT.vehicle_id
            JOIN DIMENSIONS ON VEHICLES.vehicle_id = DIMENSIONS.vehicle_id
            JOIN ENGINE ON VEHICLES.vehicle_id = ENGINE.vehicle_id
            JOIN TRASMISSION ON VEHICLES.vehicle_id = TRASMISSION.vehicle_id
            JOIN PERFORMANCE ON VEHICLES.vehicle_id = PERFORMANCE.vehicle_id
            JOIN OVERVIEW ON VEHICLES.vehicle_id = OVERVIEW.vehicle_id '''
              
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

    sql = ''' SELECT * FROM VEHICLES '''
              
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

    sql = ''' SELECT * FROM LAPS WHERE (track_id = ?) AND (vehicle_id = ?)  '''
              
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

    by_id = "track_id = ?"
    by_name = "track_name = ?"
              
    if (track_id != -1):
        sql = f''' SELECT * FROM TRACKS WHERE {by_id} '''
    else:
        sql = f''' SELECT * FROM TRACKS WHERE {by_name} '''

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

    by_id = "vehicle_id = ? "
    by_name = "vehicle_name = ?"

    cur = conn.cursor()

    joins = ''' JOIN LAYOUT ON VEHICLES.vehicle_id = LAYOUT.vehicle_id
                JOIN DIMENSIONS ON VEHICLES.vehicle_id = DIMENSIONS.vehicle_id
                JOIN ENGINE ON VEHICLES.vehicle_id = ENGINE.vehicle_id
                JOIN TRASMISSION ON VEHICLES.vehicle_id = TRASMISSION.vehicle_id
                JOIN PERFORMANCE ON VEHICLES.vehicle_id = PERFORMANCE.vehicle_id
                JOIN OVERVIEW ON VEHICLES.vehicle_id = OVERVIEW.vehicle_id '''
    
    if (vehicle_id != -1):
        sql = f''' SELECT * FROM VEHICLES 
        {joins} 
        WHERE {by_id} '''
        cur.execute(sql, (vehicle_id, ))
    else:
        sql = f''' SELECT * FROM VEHICLES
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

    by_id = "vehicle_id = ?"
    by_name = "vehicle_name = ?"
    
    cur = conn.cursor()

    if (vehicle_id != -1):
        sql = f''' SELECT * FROM VEHICLES WHERE {by_id} '''
        cur.execute(sql, (vehicle_id, ))
    else:
        sql = f''' SELECT * FROM VEHICLES WHERE {by_name} '''
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
    
    sql = ''' DELETE FROM LAPS WHERE (track_id = ?) AND (vehicle_id = ?) '''
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
        sql = f''' DELETE FROM TRACKS WHERE {by_id} '''
    else:
        sql = f''' DELETE FROM TRACKS WHERE {by_name} '''

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
    
    by_id = "vehicle_id = ?"
    by_name = "vehicle_name = ?"

    if (vehicle_id != -1):
        sql = f''' DELETE FROM VEHICLES WHERE {by_id} '''
    else:
        sql = f''' DELETE FROM VEHICLES WHERE {by_name} '''

    cur = conn.cursor()
    cur.execute(sql, (vehicle_id, vehicle_name))
    cur.close()

    conn.commit()

    print("Delete: " + vehicle_name)

def update_specific_lap(conn: sqlite3.Connection, track_id: int, vehicle_id: int, values: dict):
    # Update a lap by track name and vehicle name
    # :param conn: db connection.
    # :param track_id: track id.
    # :param vehicle_id: vehicle id.
    # :param values: a dict with key are the column list to set and values are the new values set.
    # :return:

    raise NotImplementedError
    
def update_specific_track(conn: sqlite3.Connection, track_id: str, values: dict):
    # Update a track by track name
    # :param conn: db connection.
    # :param track_id: track id.
    # :param values: a dict with key are the column list to set and values are the new values set.
    # :return:

    raise NotImplementedError

def update_specific_vehicle(conn: sqlite3.Connection, vehicle_id: str, values: dict):
    # Update a vehicle by vehicle name
    # :param conn: db connection.
    # :param vehicle_id: vehicle id.
    # :param values: a dict with key are the column list to set and values are the new values set.
    # :return:

    cur = conn.cursor()

    column_list = ", ".join([f"{column}=?" for column in values['Layout'].keys()])
    sql = f''' "UPDATE LAYOUT SET {column_list} WHERE vehicle_id = ? '''
    cur.execute(sql, (*values['Layout'].values(), vehicle_id))
    print("Update" + sql)

    column_list = ", ".join([f"{column}=?" for column in values['Dimensions'].keys()])
    sql = f''' "UPDATE DIMENSIONS SET {column_list} WHERE vehicle_id = ? '''
    cur.execute(sql, (*values['Dimensions'].values(), vehicle_id))
    print("Update" + sql)

    column_list = ", ".join([f"{column}=?" for column in values['Engine'].keys()])
    sql = f''' "UPDATE ENGINE SET {column_list} WHERE vehicle_id = ? '''
    cur.execute(sql, (*values['Engine'].values(), vehicle_id))
    print("Update" + sql)

    column_list = ", ".join([f"{column}=?" for column in values['Trasmission'].keys()])
    sql = f''' "UPDATE TRASMISSION SET {column_list} WHERE vehicle_id = ? '''
    cur.execute(sql, (*values['Trasmission'].values(), vehicle_id))
    print("Update" + sql)

    column_list = ", ".join([f"{column}=?" for column in values['Performance'].keys()])
    sql = f''' "UPDATE PERFORMANCE SET {column_list} WHERE vehicle_id = ? '''
    cur.execute(sql, (*values['Performance'].values(), vehicle_id))
    print("Update" + sql)

    column_list = ", ".join([f"{column}=?" for column in values['Overview'].keys()])
    sql = f''' "UPDATE OVERVIEW SET {column_list} WHERE vehicle_id = ? '''
    cur.execute(sql, (*values['Overview'].values(), vehicle_id))
    print("Update" + sql)
    conn.commit()
    cur.close()

    print("Update done.")
