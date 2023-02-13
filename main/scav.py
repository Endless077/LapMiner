#  ____    ____      _      _____ ____  _____  
# |_   \  /   _|    / \    |_   _|_   \|_   _| 
#   |   \/   |     / _ \     | |   |   \ | |   
#   | |\  /| |    / ___ \    | |   | |\ \| |   
#  _| |_\/_| |_ _/ /   \ \_ _| |_ _| |_\   |_  
# |_____||_____|____| |____|_____|_____|\____| of scav script...

# IMPORT
import re
import os
import sys
import json
import csv

from datetime import datetime as dt
import urllib.parse

sys.path.append("../LapMiner/fastestlaps")
sys.path.append("../LapMiner/generator")
sys.path.append("../LapMiner/sources")
sys.path.append("../LapMiner/")

sys.dont_write_bytecode = True

from sources.UltimateSpecs import UltimateSpecs
from sources.CarsData import CarsData 
from sources.Wikidata import Wikidata

import fastestlaps_db as old_db
import database as new_db
import utils

PATH = "../LapMiner/update"
SOURCES = ["ultimatespecs","cars-data","wikipedia"]

# Defination MAIN
def main():

    # Logging
    Logger = utils.Logger("update", "logs")
    sys.stdout = Logger
    sys.stderr = Logger

    # Print logo
    printLogo()

    # Create a random user agent generator
    utils.USER_AGENT = utils.random_user_agent()

    # Crate a random proxy server list
    #utils.PROXY_LIST = utils.random_proxy_list()

    # Input control and main menù
    data = dict()

    print("######################")

    # Control number of arguments
    if len(sys.argv) == 2:
        # Passed a file, check if file is a csv compliant with policy
        print("CSV file retrieve mode.")
        check_args(sys.argv[1])
        filename = sys.argv[1]
        # Open and read the CSV file
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            # Open a simple menù for choose attributes to retrive
            attr = choose_attr()
            for row in reader:
                vehicle = row[0]
                url = row[1]
                # Check if the url is a legit url
                source = check_url(url)
                try:
                    if source:
                        if check_vehicle(vehicle):
                            print(f"Vehicle {vehicle} at source {source} in retrive...")
                            # Starting the retrive of current couple of values
                            data[vehicle] = retrieve(url, source, attr)
                            update(vehicle, data[vehicle])
                            print("######################")
                        else:
                            raise SyntaxError(f"The vehicle {vehicle} not exists in database, please check.")
                    else:
                        raise SyntaxError(f"Source {source} not supported.")
                except SyntaxError as e:
                    print(f"{e}\n this record {vehicle} at this URL {url} will be skipped.")
                except ValueError as e:
                    print(f"{e}\n this record {vehicle} at this URL {url} will be skipped.")
    elif len(sys.argv) == 3:
        # Passed a couple vehicle_name/url, check if are not number or other type
        print("Vehicle and URL retrieve mode.")
        check_args(sys.argv[1], sys.argv[2])
        vehicle = sys.argv[1]
        url = sys.argv[2]
        # Check if the url is a legit url
        source = check_url(url)
        # Open a simple menù for choose attributes to retrive
        attr = choose_attr()
        if source:
            if check_vehicle(vehicle):
                print(f"Vehicle {vehicle} at source {source} in retrive...")
                # Starting the retrive of the given couple of values
                data[vehicle] = retrieve(url, source, attr)
                update(vehicle, data[vehicle])
                print("######################")
            else:
                raise SyntaxError(f"The vehicle {vehicle} not exists in database, please check.")
        else:
            raise SyntaxError(f"Source {source} not supported.")

    else:
        raise SyntaxError("Error call the scav.py script. Usage: scav.py vehicle_name source_url | file.csv")
    
    # Convert the data dictionary with all update in json
    if(not os.path.exists(PATH)):
        os.mkdir(PATH)

    curr_date = dt.now().isoformat()
    json_object_update = json.dumps(data, ensure_ascii=False, indent = 3)

    with open(f"{PATH}/update_scav{curr_date}.json", "w") as outfile:
        outfile.write(json_object_update)
    
    # Close logging
    sys.stdout.log.close()
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
    
def check_args(arg1, arg2=None):
    # Create all tables of database
    # :param arg1: arg 1 is a file (if arg2 is not declared) or the vehicle name.
    # :param arg2: arg 2 is a valid url.
    # :return:

    if arg2:
        if not isinstance(arg1, str) or not isinstance(arg2, str):
            raise SyntaxError("The given params are not string.")
    else:
        if os.path.isfile(arg1) and arg1.endswith('.csv'):
            with open(arg1, 'r') as file:
                first_line = file.readline().strip().split(',')
                if len(first_line) != 2:
                    raise SyntaxError("The CSV file don't respect policy (only 2 column).")
        else:
            raise FileNotFoundError("The file path don't exist.")

def check_vehicle(vehicle: str):
    # Check if the vehicle name is present in both database (dump.db and database.db)
    # :param vehicle: arg 1 is a file (if arg2 is not declared) or the vehicle name.
    # :return: the boolean and to both check.

    print("Validation the vehicle existence...")
    check1 = utils.checkSQLite(utils.get_SQLite_connection(old_db.PATH), "VEHICLE", "vehicle_name", vehicle)
    check2 = utils.checkSQLite(utils.get_SQLite_connection(new_db.PATH), "VEHICLE", "vehicle_name", vehicle)
    return check1 and check2

def check_url(url: str):
    # Check if the given url is a valid url and estract hostname
    # :param url: a valid url string.
    # :return: the hostname or None.

    print("Validation the URL policy...")
    regex = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if re.match(regex, url):
        parsed_url = urllib.parse.urlparse(url)
        hostname = parsed_url.hostname.split(".")[-2]
        print(f"The URL source is: {hostname}")
        return hostname if hostname in SOURCES else None
    else:
        raise SyntaxError("Invalid URL.")

def choose_attr():
    # Popup a simple choose menù to get the information
    # :param:
    # :return: a set of the chosen attributes.

    print("######################")

    print("Choose a mode:")
    print("1. Custom")
    print("2. All")
    print("3. Cancel")
    choice = input("Enter the number of your choice: ")

    try:
        choice = int(choice)
    except ValueError:
        raise Exception("Invalid choice. Enter an integer.")

    default_modes = {"Layout", "Dimensions", "Engine", "Trasmission", "Performance", "Overview"}

    if choice == 1:
        selected_modes = set()
        print("Select up to 6 modes (maximum 6 available). To stop selection, enter 'stop'.")
        print("Available modes:", ", ".join(default_modes))
        while len(selected_modes) < 6:
            mode = input("Enter the name of the mode: ")
            if mode == "stop":
                if(len(selected_modes) == 0):
                   print("Invalid custom options, please choose one or more options.")
                   continue
                else:
                    break
            if mode not in selected_modes and mode in default_modes:
                selected_modes.add(mode)
            elif(mode not in default_modes):
                print("The input mode is not in default modes.")
            elif(mode in selected_modes):
                print("Mode already selected or invalid. Select another mode.")
        print(f"The set of the chosen categories is: {selected_modes}")
        print("######################")
        return selected_modes
    elif choice == 2:
        print(f"The set of the chosen categories is: {default_modes}")
        print("######################")
        return default_modes
    elif choice == 3:
        raise SyntaxError("Operation cancelled.")
    else:
        raise SyntaxError("Invalid choice. Try again.")

def retrieve(url: str, source: str, attr: set):
    # Retrieve all information declared in attr at specific source, url and vehiclen
    # :param vehicle: vehichle name string.
    # :param url: url where get the vehicle specs.
    # :param source: a specific source.
    # :param attr: set of all attributes to retrieve.
    # :return: a dict of vehicle specs from the given source.
    
    if source == "ultimatespecs":
        us = UltimateSpecs()
        return us.get_specs(url, attr)
    elif source == "cars-data":
        cd = CarsData()
        return cd.get_specs(url, attr)
    elif source == "wikipedia":
        wiki = Wikidata()
        return wiki.get_specs(url, attr)
    else:
        raise ValueError("Invalid source. Try again.")

def update(vehicle: str, new_specs: dict):
    conn = utils.get_SQLite_connection(new_db.PATH)

    if(not new_specs):
        ValueError("Impossible to retrive information, the specs map was empty.")

    vehicle_data = new_db.get_specific_vehicle(conn, -1, vehicle)
    new_db.update_specific_vehicle(conn, vehicle_data[0], new_specs)

def printLogo():
    print("  ______     ______       _  ____   ____ ") 
    print(".' ____ \  .' ___  |     / \|_  _| |_  _|") 
    print("| (___ \_|/ .'   \_|    / _ \ \ \   / /  ") 
    print(" _.____`. | |          / ___ \ \ \ / /   ") 
    print("| \____) |\ `.___.'\ _/ /   \ \_\ ' /    ") 
    print(" \______.' `.____ .'|____| |____|\_/     ")  

# Definition NAME
if __name__ == "__main__":
    main()