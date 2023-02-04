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

import urllib.parse
from datetime import datetime as dt
from random_user_agent.user_agent import UserAgent

sys.path.append("../Lap-Time-Prediction/fastestlaps")
sys.path.append("../Lap-Time-Prediction/generator")
sys.path.append("../Lap-Time-Prediction/sources")
sys.path.append("../Lap-Time-Prediction/")

import ultimatespecs as us
import cars_data as cd
import wikidata as wiki
import database as db
import utils

PATH = "../Lap-Time-Prediction/update"
SOURCES = ["ultimatespecs","cars-data","wikipedia"]

# Defination MAIN
def main():

    # Logging
    sys.stdout = utils.Logger("update", "logs")

    printLogo()

    # Create a user-agent generator
    user_agent_generator = utils.random_user_agent()

    # Input control and main menù
    data = dict()

    if len(sys.argv) == 1:
        check_args(sys.argv[1])
        filename = sys.argv[1]
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            attr = choose_attr()
            for row in reader:
                vehicle = row[0]
                url = row[1]
                source = check_url(url)
                try:
                    if source:
                        if check_vehicle(vehicle):
                            user_agent = user_agent_generator.get_random_user_agent()
                            data[vehicle]["Update"] = retrieve(user_agent, vehicle, url, source, attr)
                            data[vehicle]["Old"] = update(vehicle, data[vehicle])
                        else:
                            raise SyntaxError(f"The vehicle {vehicle} not exists in database, please check.")
                    else:
                        raise SyntaxError(f"Source {source} not supported.")
                except SyntaxError as e:
                    print(f"{e}\n this record {vehicle} at this URL {url} will be skipped.")
                except ValueError as e:
                    print(f"{e}\n this record {vehicle} at this URL {url} will be skipped.")
    elif len(sys.argv) == 2:
        check_args(sys.argv[1], sys.argv[2])
        vehicle = sys.argv[1]
        url = sys.argv[2]
        source = check_url(url)
        attr = choose_attr()
        if source:
            if check_vehicle(vehicle):
                user_agent = user_agent_generator.get_random_user_agent()
                data[vehicle]["Update"] = retrieve(user_agent, vehicle, url, source, attr)
                data[vehicle]["Old"] = update(vehicle, data[vehicle])
            else:
                raise SyntaxError(f"The vehicle {vehicle} not exists in database, please check.")
        else:
            raise SyntaxError(f"Source {source} not supported.")

    else:
        raise SyntaxError("The script should have only 1 or 2 arguments.\
            Usage: scav.py vehicle_name source_url | file.csv")

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

    check1 = utils.checkSQLite(utils.get_SQLite_connection(old_db.PATH), "VEHICLES", "vehicle_name", vehicle)
    check2 = utils.checkSQLite(utils.get_SQLite_connection(new_db.PATH), "VEHICLES", "vehicle_name", vehicle)
    return check1 and check2

def check_url(url: str):
    # Check if the given url is a valid url and estract hostname
    # :param url: a valid url string.
    # :return: the hostname or None.

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
        return hostname if hostname in SOURCES else None
    else:
        raise SyntaxError("Invalid URL.")

def choose_attr():
    # Popup a simple choose menù to get the information
    # :param:
    # :return: a set of the chosen attributes.

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
                break
            if mode not in selected_modes and mode in default_modes:
                selected_modes.add(mode)
            else:
                print("Mode already selected or invalid. Select another mode.")
        return selected_modes
    elif choice == 2:
        return default_modes
    elif choice == 3:
        raise SyntaxError("Operation cancelled.")
    else:
        raise SyntaxError("Invalid choice. Try again.")

def retrieve(user_agent: UserAgent, vehicle: str, url: str, source: str, attr: set):
    # Retrieve all information declared in attr at specific source, url and vehiclen
    # :param user_agent: a random generated user agent.
    # :param vehicle: vehichle name string.
    # :param url: url where get the vehicle specs.
    # :param source: a specific source.
    # :param attr: set of all attributes to retrieve.
    # :return: a dict of vehicle specs from the given source.
    
    if source == "ultimatespecs":
        return us.get_specs(user_agent, vehicle, url, attr)
    elif source == "cars-data":
        return cd.get_specs(user_agent, vehicle, url, attr)
    elif source == "wikipedia":
        return wiki.get_specs(user_agent, vehicle, url, attr)
    else:
        raise ValueError("Invalid source. Try again.")

def update(vehicle: str, new_specs: dict):
    conn = utils.get_SQLite_connection(db.PATH)

    vehicle_data = db.get_specific_vehicle(conn, -1, vehicle)
    curr_specs = db.get_specific_vehicle_specs(conn, vehicle_data[0], vehicle)

    db.update_specific_vehicle(conn, vehicle_data[0], new_specs)

    old_specs = dict()
    return old_specs

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