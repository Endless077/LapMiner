# Ecco il main del progetto :)

# IMPORT
import sys
import os

sys.path.append("./Fastestlaps")

import fastestlaps_db as db
import fastestlaps_scrap as scrap

# Defination MAIN
def main():
   # Create database (if exist, delete and create)
   if os.path.exists(db.PATH):
    os.remove(db.PATH)
   
   print("######################")
   db.create_database()
   conn =  db.get_connection()
   db.create_tables(conn)

   # Scraping from fastestlaps.com
   all_tracks = scrap.get_all_tracks()
   print("######################")
   print("Initial laps scraping:")
   for track in all_tracks:
      laps = scrap.get_laps_time(track)
      track = (track['name'], track['href'])
      print("######################")
      print("Initial laps record creator:")
      scrap.record_creator(laps, track)
      print("######################")
      
   # Delete all motobike
   # delete all motobike from dataset database

# Definition NAME
if __name__ == "__main__":
    main()