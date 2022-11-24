# Ecco il main del progetto :)

# IMPORT
import sys
import os

sys.path.append("./Fastestlaps")

import fastestlaps_db as db
import fastestlaps_scrap as scrap

# Defination MAIN
def main():
   # Create database (if exist, delete and create).
   if os.path.exists(db.PATH):
    os.remove(db.PATH)
   
   print("######################")
   db.create_database()
   conn =  db.get_connection()
   db.create_tables(conn)
   print("######################")
   
   # Scraping from fastestlaps.com,
   # first phase: getting all track name and href.
   all_tracks = scrap.get_all_tracks()
   print("######################")
   
   # Scraping from fastestlaps.com,
   # second phase: getting all track information (i.e Country, length and all laps).
   print("Initial laps scraping:")
   for track in all_tracks:
      value = scrap.get_track_info(track)
      laps = value['laps_time']
      track = (track['name'], track['href'], value['track_info'][0], value['track_info'][1][0])
      print("######################")

      # Adding in sqlite database all scraps,
      # third phase: adding all info and laps of current track.
      print("Initial laps record creator:")
      scrap.record_creator(laps, track)
      print("######################")

   # Scraping from fastestlaps.com,
   # fourth phase: getting all vehicle information (i.e Country, power, etc...).
   
# Definition NAME
if __name__ == "__main__":
    main()