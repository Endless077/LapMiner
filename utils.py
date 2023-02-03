#  _____  _____ _________ _____ _____     ______   
# |_   _||_   _|  _   _  |_   _|_   _|  .' ____ \  
#   | |    | | |_/ | | \_| | |   | |    | (___ \_| 
#   | '    ' |     | |     | |   | |   _ _.____`.  
#    \ \__/ /     _| |_   _| |_ _| |__/ | \____) | 
#     `.__.'     |_____| |_____|________|\______.' 

import re
import requests
import contextlib
import os
import sys

import sqlite3
from sqlite3 import Error

from bs4 import BeautifulSoup

from datetime import datetime as dt

from random_user_agent.params import HardwareType, SoftwareEngine, SoftwareName, SoftwareType, OperatingSystem, Popularity
from random_user_agent.user_agent import UserAgent

# Logging class
class Logger(object):
    def __init__(self):
        if not os.path.exists("./logs"):
            os.mkdir("./logs")
        curr_date = dt.now().isoformat()
        self.terminal = sys.stdout
        self.log = open(f"./logs/logging_{curr_date}.txt", "x")

    def __init__(self, file, dir):
        if not os.path.exists(f"./{dir}"):
            os.mkdir(f"./{dir}")
        curr_date = dt.now().isoformat()
        self.terminal = sys.stdout
        self.log = open(f"./{dir}/{file}_{curr_date}.txt", "x")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
        
    def flush(self):
        self.terminal.flush()
        self.log.flush()


# Database SQLite
def checkSQLite(conn: sqlite3.Connection, table: str, attr: str, value_attr: str):
    # Check if exist a record in table where attr is equal to value
    # :param conn: database connection.
    # :param value: value string.
    # :param table: table name string.
    # :param attr: attribute name string.
    # :return: result object or None.

    cur = conn.cursor()
    
    cur.execute(f"SELECT * FROM {table} WHERE {attr}=?", (value_attr,))
    result = cur.fetchone()
    
    conn.close()
    
    return result is not None

def create_SQLite_database(PATH):
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

def get_SQLite_connection(PATH):
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

# Database MySQL
def check_MySQL(conn: sqlite3.Connection, table: str, attr: str, value_attr: str):
    raise NotImplementedError

def create_MySQL_database(PATH):
    raise NotImplementedError

def get_MySQL_connection(PATH):
    raise NotImplementedError

# Database PostgreSQL
def check_PostgreSQL(conn: sqlite3.Connection, table: str, attr: str, value_attr: str):
    raise NotImplementedError

def create_PostgreSQL_database(PATH):
    raise NotImplementedError

def get_PostgreSQL_connection(PATH):
    raise NotImplementedError

# Some utils
def random_user_agent():
    user_agent_rotator = None

    hardwareTypes =         [HardwareType.COMPUTER.value, HardwareType.MOBILE.value]
    softwareEngines =       [SoftwareEngine.GECKO.value, SoftwareEngine.BLINK.value, SoftwareEngine.WEBKIT.value] 
    softwareNames =         [SoftwareName.EDGE.value, SoftwareName.FIREFOX.value, SoftwareName.CHROME.value, SoftwareName.BRAVE.value]
    softwareTypes =         [SoftwareType.APPLICATION.value]
    operatingSystems =      [OperatingSystem.LINUX.value, OperatingSystem.IOS.value, OperatingSystem.ANDROID.value, OperatingSystem.WINDOWS.value]
    popularity_services =   [Popularity.UNCOMMON.value, Popularity.COMMON.value, Popularity.POPULAR.value, Popularity.AVERAGE.value]

    user_agent_rotator = UserAgent(hardware_type=hardwareTypes, operating_system=operatingSystems, software_type=softwareTypes,
                                software_name=softwareNames, software_engine=softwareEngines, popularity=popularity_services,
                                limit=100)

    return user_agent_rotator

def html_downloader():
    LINK = []
    HEADERS = {
    'User-Agent': 'user-agent',
    "Content-Type": "text/html"
    # other headers allowed.
    }

    user_agent_generator = random_user_agent()

    for site in LINK:
        try:
            HEADERS["User-Agent"] = user_agent_generator.get_random_user_agent()
            response = requests.get(site, headers=HEADERS, timeout=10)
            response.raise_for_status()
        except requests.ConnectionError as e:
            print("Error (connection):")
            print(e)
        except requests.Timeout as e:
            print("Error (timeout):")
            print(e)
        except requests.HTTPError as e:
            print("Error (http):")
            print(e)
        except:
            print("Someting goes wrong here.")
        else:
            print("HTTP Status request: " + str(response.status_code))
            
            if not os.path.exists("./Temp"):
                os.mkdir("./Temp")
            path = "./Temp/" + site + ".html"
            with open(path, 'x') as f:
                f.write(response.text)

def image_downloader():
    LINK = []
    HEADERS = {
    'User-Agent': 'user-agent',
    "Content-Type": "text/html"
    # other headers allowed.
    }

    user_agent_generator = random_user_agent()

    for site in LINK:
        try:
            HEADERS["User-Agent"] = user_agent_generator.get_random_user_agent()
            response = requests.get(site, headers=HEADERS, timeout=10)
            response.raise_for_status()
        except requests.ConnectionError as e:
            print("Error (connection):")
            print(e)
        except requests.Timeout as e:
            print("Error (timeout):")
            print(e)
        except requests.HTTPError as e:
            print("Error (http):")
            print(e)
        except:
            print("Someting goes wrong here.")
        else:
            print("HTTP Status request: " + str(response.status_code))
            
            if not os.path.exists("./Temp"):
                os.mkdir("./Img")
            response = request(site, HEADERS, 10)
            soup = BeautifulSoup(response.text, "html.parser")
            imgs = soup.find_all("img")
            for img in imgs:
                alt_info = img['alt']
                image_name = f"{alt_info}.png"
                url_info = f"{site}{img['content']}"
        
                with contextlib.closing(requests.get(url_info)) as image:
                    path = "./Img/" + image_name
                    with open(path,"wb") as dest_file:
                        for block in image.iter_content(1024):
                            if block:
                                dest_file.write(block)
                    dest_file.close()     

def request(link, headers, timeout):
    try:
        response = requests.get(link, headers=headers, timeout=timeout)
        response.raise_for_status()
    except requests.ConnectionError as e:
        print("Error (connection):")
        print(e)
    except requests.Timeout as e:
        print("Error (timeout):")
        print(e)
    except requests.HTTPError as e:
        print("Error (http):")
        print(e)
    except:
            print("Someting goes wrong here.")
    else:
        print("HTTP Status request: " + str(response.status_code))
    
    return response
