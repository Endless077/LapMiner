#  ____    ____      _      _____ ____  _____  
# |_   \  /   _|    / \    |_   _|_   \|_   _| 
#   |   \/   |     / _ \     | |   |   \ | |   
#   | |\  /| |    / ___ \    | |   | |\ \| |   
#  _| |_\/_| |_ _/ /   \ \_ _| |_ _| |_\   |_  
# |_____||_____|____| |____|_____|_____|\____| of report script...

# IMPORT
import os
import sys
import shutil

sys.path.append("../LapMiner/fastestlaps")
sys.path.append("../LapMiner/generator")
sys.path.append("../LapMiner/")

sys.dont_write_bytecode = True

import fastestlaps_db as old_db
import database as new_db
import verbose
import utils

# Defination MAIN
def main():

    # Logging
    sys.stdout = utils.Logger("report", "logs")

    # Print logo
    printLogo()
    
    # Create folders tree (if exist, delete and create)
    check_tree_struct()

    # Upgrade database
    print("######################")
    while True:
        print("Upgrade dump.db, do you want skip upgrade function, it will takes more than 5 minutes? (yes/no)")
        skip = input("WARNING: if exist the database will be reset at default fastestlaps value, if not exist a FileNotFound exception will raise.\n")
        print(f"Upgrade? {skip}")
        print("######################")
        try:
            if(skip.lower() == "yes"):
                if not os.path.exists(new_db.FOLDER):
                    os.mkdir(new_db.FOLDER)
                if os.path.exists(new_db.PATH):
                    os.remove(new_db.PATH)
                new_db.upgrade(old_db.PATH)
                break
            elif(skip.lower() == "no"):
                break
            else:
                raise ValueError
        except ValueError:
            print("Error input, insert a valid value.")

    if not os.path.exists(new_db.PATH):
        raise FileNotFoundError("No database.db found.")
    
    # Create TEMP view to get a filtered dataset
    conn = verbose.extract_dataset()
    
    # Generate excel, csv and json file format of all filtered dataset
    verbose.dataset_generator(conn)
    print("######################")

    # Create a stats report
    verbose.report()
    print("######################")
    
    # Create a matrix output (exemple that contains "Unknown")
    tracks = ["Unknown","Balocco","Le Mans (Bugatti)","Nürburgring Nordschleife",
    "Hockenheim Short","Laguna Seca (Post 1988)","Top Gear Track",
    "Sachsenring","Circuit De Nevers Magny-Cours Club","Ring Knutstrop (Conf 2)",
    "Vairano Handling Course"]
    verbose.matrix_generator(tracks)
    print("######################")
    
    # Close database connection
    conn.close()
    
    # Close logging
    sys.stdout.log.close()
    sys.stdout = sys.__stdout__

def check_tree_struct():
    paths = [verbose.PATH + "/csv", verbose.PATH + "/excel", verbose.PATH + "/json", verbose.PATH + "/matrix"]

    if(not os.path.exists(verbose.PATH)):
        os.mkdir(verbose.PATH)
    
    for path in paths:
            if(not os.path.exists(path)):
                os.mkdir(path)
            else:
                shutil.rmtree(path)
                os.mkdir(path)

def printLogo():
    print("  _______    ________ _______    ___  _______  _________  ") 
    print(" |_   __ \  |_   __  |_   __ \ .'   `|_   __ \|  _   _  | ") 
    print("   | |__) |   | |_ \_| | |__) /  .-.  \| |__) |_/ | | \_| ") 
    print("   |  __ /    |  _| _  |  ___/| |   | ||  __ /    | |     ") 
    print("  _| |  \ \_ _| |__/ |_| |_   \  `-'  _| |  \ \_ _| |_    ") 
    print(" |____| |___|________|_____|   `.___.|____| |___|_____|   ")

# Definition NAME
if __name__ == "__main__":
    main()
