# Ecco il main del progetto :)

# IMPORT
import Fastestlaps.fastestlaps_db
import Fastestlaps.fastestlaps_scrap

# Defination MAIN
def main():
   # Create database
   Fastestlaps.fastestlaps_db.create_database()
   conn =  Fastestlaps.fastestlaps_db.get_connection()
   Fastestlaps.fastestlaps_db.create_tables(conn)

   # Scraping from fastestlaps.com
   all_tracks = Fastestlaps.fastestlaps_scrap.get_all_tracks()

   for track in all_tracks:
      laps = Fastestlaps.fastestlaps_scrap.get_laps_time(track)
      track = (track['name'], track['HRef'])
      Fastestlaps.fastestlaps_scrap.record_createor(laps, track)

# Definition NAME
if __name__ == "__main__":
    main()