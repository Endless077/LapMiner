#  _____  _____ _________ _____ _____     ______   
# |_   _||_   _|  _   _  |_   _|_   _|  .' ____ \  
#   | |    | | |_/ | | \_| | |   | |    | (___ \_| 
#   | '    ' |     | |     | |   | |   _ _.____`.  
#    \ \__/ /     _| |_   _| |_ _| |__/ | \____) | 
#     `.__.'     |_____| |_____|________|\______.' 

import re
import random
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

# Global variables
USER_AGENT = None

HEADERS = {
    'User-Agent': 'user-agent',
    'Accept-Language': 'en-US;q=0.5,en;q=0.3,it-IT,it;q=0.8',
    'Accept-Encoding': 'gzip',
    'Referer': 'https://www.google.com',
    'DNT': '1',
    'Connection': 'keep-alive',
    'TE': 'Trailers'
}

PROXY_LIST_HTTP = []
PROXY_LIST_HTTPS = []

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

    print(f"Getting database {PATH} connection...")

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
    # Create a random user_agent generator
    # :param:
    # :return:

    user_agent_rotator = None

    hardwareTypes =         [HardwareType.COMPUTER.value, HardwareType.MOBILE.value]
    softwareEngines =       [SoftwareEngine.GECKO.value, SoftwareEngine.BLINK.value, SoftwareEngine.WEBKIT.value] 
    softwareNames =         [SoftwareName.EDGE.value, SoftwareName.FIREFOX.value, SoftwareName.CHROME.value, SoftwareName.BRAVE.value]
    softwareTypes =         [SoftwareType.APPLICATION.value]
    operatingSystems =      [OperatingSystem.LINUX.value, OperatingSystem.IOS.value, OperatingSystem.ANDROID.value, OperatingSystem.WINDOWS.value]
    popularity_services =   [Popularity.COMMON.value, Popularity.POPULAR.value, Popularity.AVERAGE.value]

    user_agent_rotator = UserAgent(hardware_type=hardwareTypes, operating_system=operatingSystems, software_type=softwareTypes,
                                software_name=softwareNames, software_engine=softwareEngines, popularity=popularity_services,
                                limit=100)

    return user_agent_rotator

def random_proxy_list():
    # Create a random proxy list
    # :param:
    # :return:

    raise NotImplementedError

def html_downloader(sources: list):
    # Download a html list site
    # :param sources: a list of URL site.
    # :return:

    if(not USER_AGENT):
        USER_AGENT.random_user_agent()
        
    user_agent = USER_AGENT.get_random_user_agent()
    HEADERS["User-Agent"] = user_agent
    
    proxy = PROXY_LIST[random.randint(0, len(PROXY_LIST) - 1)]
    proxies = {
        "http": proxy.host,
        "https": proxy.host,
    }

    for site in sources:
        response = requests.get(site, headers=HEADERS, proxies=proxies, timeout=10)
        try:
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

def image_downloader(sources: list):
    # Download a image list source
    # :param sources: a list of URL image.
    # :return:

    if(not USER_AGENT):
        USER_AGENT.random_user_agent()

    user_agent = USER_AGENT.get_random_user_agent()
    HEADERS["User-Agent"] = user_agent
    
    proxy = PROXY_LIST[random.randint(0, len(PROXY_LIST) - 1)]
    proxies = {
        "http": proxy.host,
        "https": proxy.host,
    }
    
    for uri in sources:
        response = requests.get(uri, headers=HEADERS, proxies=proxies, timeout=10)
        try:
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

def request(url: str, timeout: int):
    # Create a get http/https request and return the response (print the error)
    # :param url: a given url site to request.
    # .param timeout: a given int timeout.
    # :return: a response objcet from requests library.
    
    if(not USER_AGENT):
        USER_AGENT.random_user_agent()

    user_agent = USER_AGENT.get_random_user_agent()
    HEADERS["User-Agent"] = user_agent

    if(len(PROXY_LIST_HTTP) > 0 and len(PROXY_LIST_HTTPS) > 0):
        proxyhttp = PROXY_LIST_HTTP[random.randint(0, len(PROXY_LIST_HTTP) - 1)]
        proxyhttps = PROXY_LIST_HTTPS[random.randint(0, len(PROXY_LIST_HTTPS) - 1)]
        proxies = {
            'http': proxyhttp,
            'https': proxyhttps
        }
        response = requests.get(url, headers=HEADERS, proxies=proxies, timeout=timeout)
    else:
        response = requests.get(url, headers=HEADERS, timeout=timeout)

    try:
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
