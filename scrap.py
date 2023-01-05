#  ____    ____      _      _____ ____  _____  
# |_   \  /   _|    / \    |_   _|_   \|_   _| 
#   |   \/   |     / _ \     | |   |   \ | |   
#   | |\  /| |    / ___ \    | |   | |\ \| |   
#  _| |_\/_| |_ _/ /   \ \_ _| |_ _| |_\   |_  
# |_____||_____|____| |____|_____|_____|\____| of scraping script...

# IMPORT
import os
import sys
import time

sys.path.append("./Fastestlaps")

import fastestlaps_db as db
import fastestlaps_scrap as scrap
import utils

# Defination MAIN
def main():

   # Logging
   sys.stdout = utils.Logger("scraping", "logs")

   # Print logo
   printLogo()

   # Create database (if exist, delete and create).
   if os.path.exists(db.PATH):
    os.remove(db.PATH)
   
   print("######################")
   db.create_database()
   conn =  db.get_connection()
   db.create_tables(conn)
   print("######################")
   
   # Generate a user-agent generator
   user_agent_generator = utils.random_user_agent()

   # Scraping from fastestlaps.com,
   # first phase: getting all track name and href.
   user_agent = user_agent_generator.get_random_user_agent()
   all_tracks = scrap.get_all_tracks(user_agent)
   print("######################")
   
   # Scraping from fastestlaps.com,
   # second phase: getting all track information (i.e Country, length and all laps).
   print("Initial laps scraping:")
   for track in all_tracks:
      user_agent = user_agent_generator.get_random_user_agent()
      value = scrap.get_track_info(user_agent, track)
      if(value['track_info'] is not None):
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
   # fourth phase: getting all vehicle information (i.e Country, power, etc...).
   all_vehicle = db.get_all_vehicles(conn)
   for vehicle in all_vehicle:
      user_agent = user_agent_generator.get_random_user_agent()
      if(vehicle[1] != None):
         vehicle_specs = scrap.get_vehicle_info(user_agent, vehicle)
         if(len(vehicle_specs) != 1):
            extracted_specs = scrap.extract_specs(vehicle_specs)
            print("######################")
            db.insert_new_specs(conn, extracted_specs)
            print("######################")
         else:
            print(f"Error during {vehicle[0]} specs record process. Skipped.")
            print("######################")
      else:
         print(f"Vehicle {vehicle[0]} page, don't exist. Skipped.")
         print("######################")


   # Printing some scraping stats
   n_laps = len(db.get_all_laps(conn))
   n_tracks = len(db.get_all_tracks(conn))
   n_vehicles = len(db.get_all_vehicles(conn))
   
   print("######################")
   print("Laps n°: " + str(n_laps) + ".")
   print("Tracks n°: " + str(n_tracks) + ".")
   print("Vehicles n°: " + str(n_vehicles) + ".")
   print("######################")

   # Close database connection
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