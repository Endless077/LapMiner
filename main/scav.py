#  ____    ____      _      _____ ____  _____  
# |_   \  /   _|    / \    |_   _|_   \|_   _| 
#   |   \/   |     / _ \     | |   |   \ | |   
#   | |\  /| |    / ___ \    | |   | |\ \| |   
#  _| |_\/_| |_ _/ /   \ \_ _| |_ _| |_\   |_  
# |_____||_____|____| |____|_____|_____|\____| of scav script...


# Enti pubblici:
# -Automotive Industry Data
# -Ward's Automotive
# -NHTSA (National Highway Traffic Safety Administration)

# Unofficial public dataset:
# -UCI Machine Learning Repository
# -Kaggle
# -datasets.com
# -Car Dataset
# -Car Models List
# -OpenVehicles
	
# Siti di auto:
# -CarAndDriver
# -MotorTrend
# -cars-data
# -QuattroRuote
# -UltimateSpec

# API:
# -Edmunds API
# -Foursquare API
# -CarQuery API
# -AutoAPI

# IMPORT
import re
import os
import sys
import csv

sys.path.append("../Lap-Time-Prediction/Fastestlaps")
sys.path.append("../Lap-Time-Prediction/Generator")
sys.path.append("../Lap-Time-Prediction/")

import fastestlaps_db.py as old_db
import database as new_db
import utils

SOURCES = []

def main():

    printLogo()
    
    if len(sys.argv) == 1:
        check_args(sys.argv[1])
        with open(sys.argv[1], 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                vehicle = row[0]
                url = row[1]
                try:
                    if check_vehicle(sys.argv[1]):
                        source = check_url(sys.argv[2])
                        if source:
                            retrive(vehicle, url, source)
                        else:
                            raise SyntaxError(f"Source {source} not supported.")
                    else:
                        raise SyntaxError(f"The vheicle {sys.argv[1]} not exist in database, please check.")
                except SyntaxError as e:
                    print(e)

    elif len(sys.argv) == 2:
        check_args(sys.argv[1], sys.argv[2])
        if check_vehicle(sys.argv[1]):
            source = check_url(sys.argv[2])
            if source:
                retrive(sys.argv[1], sys.argv[1], source)
            else:
                raise SyntaxError(f"Source {source} not supported.")
        else:
            raise SyntaxError(f"The vheicle {sys.argv[1]} not exist in database, please check.")

    else:
        raise SyntaxError("The script should have only 1 or 2 arguments.\
            Usage: scav.py vehicle_name source_url | file.csv")
            
def check_args(arg1, arg2=None):
    if arg2:
        if isinstance(arg1, str) and isinstance(arg2, str):
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
    check1 = utils.checkSQLite(utils.get_SQLite_connection(old_db.PATH), vehicle, "VEHICLES", "vehicle_name")
    check2 = utils.checkSQLite(utils.get_SQLite_connection(new_db.PATH), vehicle, "VEHICLES", "vehicle_name")
    return check1 and check2

def check_url(url: str):
    match = re.match(r'^https?://[a-zA-Z0-9_.-]+\.[a-zA-Z]{2,}', url)
    if match:
        url_base = match.group().split("//")[1].split(".")[0]
        return url_base if url_base in SOURCES else None
    else:
       raise SyntaxError("The URL string is not a URL")

def retrive(vehicle: str, url: str, source: str):
    raise NotImplementedError

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