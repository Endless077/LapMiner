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
import time

sys.path.append("../Lap-Time-Prediction/")
sys.path.append("../Lap-Time-Prediction/Fastestlaps")

import fastestlaps_db as db
import fastestlaps_scrap as scrap
import fastestlaps_report as report
import utils

# Defination MAIN
def main():

    # Logging
    sys.stdout = utils.Logger("report", "logs")

    # Print logo
    printLogo()
    
    # Create folders tree (if exist, delete and create).
    check_tree_struct()

    print("######################")
    # Create TEMP view to get a filtered dataset
    conn = report.extract_dataset()
    
    # Generate excel, csv and json file format of all filtered dataset
    report.dataset_generator(conn)
    print("######################")

    # Create a stats report
    report.report()
    print("######################")
    
    # Create a matrix output
    report.matrix_generator()
    print("######################")
    
    # Close database connection
    conn.close()
    
    # Close logging
    sys.stdout.log.close()
    sys.stdout = sys.__stdout__

def check_tree_struct():
    paths = [report.PATH + "/csv", report.PATH + "/excel", report.PATH + "/json", report.PATH + "/matrix"]

    if(not os.path.exists(report.PATH)):
        os.mkdir(report.PATH)
    else:
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
