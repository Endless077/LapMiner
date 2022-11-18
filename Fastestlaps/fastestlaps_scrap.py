# Fastestlaps scrap

import requests
import re
import fastestlaps_db as db
from bs4 import BeautifulSoup
from urllib.error import HTTPError

LINK = "https://fastestlaps.com/tracks"
BASE_LINK = "https://fastestlaps.com/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    "Content-Type": "text/html"
    # other headers allowed.
}

def change_laptime(laptime):
    m, s = laptime.split(':')
    return int(m) * 60 + float(s)

def record_createor(laps, track):
    if(len(laps)>0):
        for lap in laps:
            vehicle = (lap['vehicle'], lap['vehilce_href'])
            laptime = change_laptime(lap['laptime'])
            lap = (laptime, lap['driver'], lap['ps_kg'], track[0], lap['vehicle'])
            db.insert_new_record(lap, track, vehicle)

def get_all_tracks():
    try:
        response = requests.get(LINK, headers=HEADERS)
        response.raise_for_status()
    except HTTPError as e:
        print(e)
    else:
        print("Status request: " + str(response.status_code))

    print("Parsing html...")
    soup = BeautifulSoup(response.text, 'html.parser')
    tag = soup.find(class_=re.compile("section"))
    tracks = tag.findAll('a')
    
    all_track = []

    print("Processing traks...")
    for track in tracks:
        new_track = {}
        new_track['name'] = track.contents[0]
        new_track['href'] = track.get('href')
        all_track.append(new_track)
        print("--New Track Found: " + new_track['name'])

    return all_track

def get_laps_time(track):
    track_link = BASE_LINK + track['href']
    try:
        response = requests.get(track_link, headers=HEADERS)
        response.raise_for_status()
    except HTTPError as e:
        print(e)
    else:
        print("Status request: " + str(response.status_code))

    print("Parsing html...")
    soup = BeautifulSoup(response.text, 'html.parser')
    tag = soup.find(class_=re.compile("table table-striped fl-laptimes-trackpage"))
    laps = tag.findAll('tr')

    check = lambda a : len(a)>0

    laps_time = []

    if(check(laps)):
        laps.pop(0)
        print("Found " + str(len(laps)) + " laps, track " + track['name'] + " processed.")
        for lap in laps:
            lap_record = lap.findAll('td')
            new_lap = {
                'laptime': str(lap_record[3].contents[0].text),
                'driver': str(lap_record[2].contents[0].text),
                'track': str(track['name']),
                'ps_kg': "".join(str(lap_record[4].contents[0]).split()),
                'vehilce_href': str(BASE_LINK + lap_record[1].contents[0].get('href')),
                'vehicle': str(lap_record[1].contents[0].text)
            }
            laps_time.append(new_lap)

    else:
        print("Found 0 laps, track " + track['name'] + " not processed.")
        return laps_time
    
