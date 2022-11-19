# Fastestlaps scrap

import requests
import re
import fastestlaps_db as db
from bs4 import BeautifulSoup
from urllib.error import HTTPError

LINK = "https://fastestlaps.com/tracks"
BASE_LINK = "https://fastestlaps.com"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    "Content-Type": "text/html"
    # other headers allowed.
}

def change_laptime(laptime):
    check = re.compile('^\d*:\d*\.\d*$')
    res = [substr for substr in laptime.split() if check.match(substr)  ]
    if(len(res)>0):
        m, s = res[0].split(':')
        return round(int(m) * 60 + float(s), 2)
    else:
        print("Impossible parsing laptime.")
        return 0.0

def record_creator(laps, track):
    if(len(laps)>0):
        for lap in laps:
            vehicle = (lap['vehicle'], lap['vehicle_href'])
            laptime = change_laptime(lap['laptime'])
            lap = (laptime, lap['driver'], lap['ps_kg'], track[0], lap['vehicle'])
            db.insert_new_record(lap, track, vehicle)

def get_all_tracks():
    try:
        response = requests.get(LINK, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except HTTPError as e:
        print(e)
    else:
        print("HTTP Status request: " + str(response.status_code))

    print("Parsing html...")
    soup = BeautifulSoup(response.text, 'html.parser')
    tag = soup.find(class_=re.compile("section"))
    tracks = tag.findAll('a')
    
    all_track = []

    print("Processing tracks...")
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
        response = requests.get(track_link, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except HTTPError as e:
        print(e)
    else:
        print("HTTP Status request: " + str(response.status_code))

    print("Parsing html...")
    soup = BeautifulSoup(response.text, 'html.parser')
    tag = soup.find(class_=re.compile("table table-striped fl-laptimes-trackpage"))

    check1 = lambda input : input!=None
    check2 = lambda chk : 1 if(chk[1].contents[0].text.strip() == "Modified") else 0

    laps_time = []

    if(check1(tag)):
        laps = tag.findAll('tr')
        laps.pop(0)
        print("--Found " + str(len(laps)) + " laps, track " + track['name'] + " processed.")
        for lap in laps:
            lap_record = lap.findAll('td')
            index_vehicle = check2(lap_record)
            
            try:    
                if(lap_record[1].contents[index_vehicle].has_attr('href')):
                    vehicle_href = lap_record[1].contents[index_vehicle].get('href')
            except:
                vehicle_href = "Non presente"
            
            vehicle_name = lap_record[1].contents[index_vehicle].text
            new_lap = {
                'laptime': str(lap_record[3].contents[0].text),
                'driver': str(lap_record[2].contents[0].text),
                'track': str("a caso"),
                'ps_kg': str("".join(str(lap_record[4].contents[0]).split())),
                'vehicle_href': str(vehicle_href),
                'vehicle': str(vehicle_name)
            }
            print("----Laptime: " + str(new_lap))
            laps_time.append(new_lap)
    else:
        print("--Found 0 laps, track " + track['name'] + " not processed.")
    
    return laps_time
    