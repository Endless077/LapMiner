# Ecco lo scrap del progetto :)

# IMPORT
import os
import sys
import shutil
import time

sys.path.append("./Fastestlaps")

import fastestlaps_db as db
import fastestlaps_scrap as scrap
import fastestlaps_report as report
import utils

import pandas as pd

# Defination MAIN
def main():

    # Logging
    sys.stdout = utils.Logger("report", "report")

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
    
    # Close database connection
    conn.close()
    
    # Close logging
    sys.stdout.log.close()
    sys.stdout = sys.__stdout__

def check_tree_struct():
    paths = [report.PATH + "/excel", report.PATH + "/csv", report.PATH + "/json"]

    if(not os.path.exists(report.PATH)):
        os.mkdir(report.PATH)
    else:
        for path in paths:
            if(not os.path.exists(path)):
                os.mkdir(path)
            else:
                shutil.rmtree(path)
                os.mkdir(path)

# Definition NAME
if __name__ == "__main__":
    main()
