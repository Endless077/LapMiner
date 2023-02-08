#  ____    ____      _      _____ ____  _____  
# |_   \  /   _|    / \    |_   _|_   \|_   _| 
#   |   \/   |     / _ \     | |   |   \ | |   
#   | |\  /| |    / ___ \    | |   | |\ \| |   
#  _| |_\/_| |_ _/ /   \ \_ _| |_ _| |_\   |_  
# |_____||_____|____| |____|_____|_____|\____| of scraping script...

# IMPORT
import os
import sys

sys.path.append("../Lap-Time-Prediction/fastestlaps")
sys.path.append("../Lap-Time-Prediction/generator")
sys.path.append("../Lap-Time-Prediction/sources")
sys.path.append("../Lap-Time-Prediction/")

sys.dont_write_bytecode = True

import fastestlaps_db as dump
import fastestlaps_scrap as scrap
import utils

# Defination MAIN
def main():

   # Logging
   sys.stdout = utils.Logger("scraping", "logs")

   # Print logo
   printLogo()

   # Create a random user agent generator
   utils.USER_AGENT = utils.random_user_agent()

   # Crate a random proxy server list
   # utils.PROXY_LIST = utils.random_proxy_list()
    
   # Create dump (if exist, delete and create).
   if os.path.exists(dump.PATH):
      os.remove(dump.PATH)
   
   print("######################")
   utils.create_SQLite_database(dump.PATH)
   conn =  utils.get_SQLite_connection(dump.PATH)
   dump.create_tables(conn)
   print("######################")

   # Scraping from fastestlaps.com,
   # first phase: getting all track name and href.
   all_tracks = scrap.get_all_tracks()
   print("######################")
   
   # Scraping from fastestlaps.com,
   # second phase: getting all track information (i.e country, length and all laps).
   print("Initial laps scraping:")
   for track in all_tracks:
      value = scrap.get_track_info(track)
      if((value['track_info'][0] is not None) and (value['track_info'][1] is not None)):
         laps = value['laps_time']
         track = (track['name'], track['href'], value['track_info'][0], value['track_info'][1][0])
         print("######################")

      # Adding in sqlite database all scraps,
      # third phase: adding all info and laps of current track.
         print("Initial laps record creator:")
         scrap.record_creator(laps, track)
         print("######################")
      else:
         print(f"Error during {track['name']} record process. Skipped.")
         print("######################")
   
   # Scraping from fastestlaps.com,
   # fourth phase: getting all vehicle specs information
   all_vehicle = dump.get_all_vehicles(conn)
   for vehicle in all_vehicle:
      if(vehicle[1] != None):
         vehicle_specs = scrap.get_vehicle_info(vehicle)
         if(len(vehicle_specs) != 1):
            extracted_specs = scrap.extract_specs(vehicle_specs)
            print("######################")
            dump.insert_new_specs(conn, extracted_specs)
            print("######################")
         else:
            print(f"Error during {vehicle[0]} specs record process. Skipped.")
            print("######################")
      else:
         print(f"Vehicle {vehicle[0]} page, don't exist. Skipped.")
         print("######################")
    
   # Printing some scraping stats
   n_laps = len(dump.get_all_laps(conn))
   n_tracks = len(dump.get_all_tracks(conn))
   n_vehicles = len(dump.get_all_vehicles(conn))
   
   print("######################")
   print("Laps n°: " + str(n_laps) + ".")
   print("Tracks n°: " + str(n_tracks) + ".")
   print("Vehicles n°: " + str(n_vehicles) + ".")
   print("######################")
   
   # Close dump database connection
   conn.close()

   # Close logging
   sys.stdout.log.close()
   sys.stdout = sys.__stdout__

def printLogo():
   print("   ______    ______ _______         _      _______   ")
   print(" .' ____ \ .' ___  |_   __ \       / \    |_   __ \  ")
   print(" | (___ \_/ .'   \_| | |__) |     / _ \     | |__) | ")
   print("  _.____`.| |        |  __ /     / ___ \    |  ___/  ")
   print(" | \____) \ `.___.'\_| |  \ \_ _/ /   \ \_ _| |_     ")
   print("  \______.'`.____ .|____| |___|____| |____|_____|    ")

# Definition NAME
if __name__ == "__main__":
    main()