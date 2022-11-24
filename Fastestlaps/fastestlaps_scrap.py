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
    res = [substr for substr in laptime.split() if check.match(substr)]
    if(len(res)>0):
        m, s = res[0].split(':')
        return round(int(m) * 60 + float(s), 2)
    else:
        print("Impossible parsing laptime.")
        return 0.0

def get_track_length(soup):
    print("Getting track length...")
    tag = soup.find(class_=re.compile("table fl-datasheet"))
    table = tag.findAll('tr')

    is_present = False
    length = ""

    for record in table:
    
        new_line_count = record.contents.count('\n')
        for i in range(new_line_count):
            record.contents.remove('\n')

        if(record.contents[0].text == 'Track length'):
            is_present = True
            length = record.contents[1].text
            break
    
    track_length = (0.0, 0.0)

    if(is_present):
        all_length = length.split('/')
        ret = []
        match = re.compile('[+-]?\d+\.\d+')
        for length in all_length:
            matches = re.findall(match, length.strip())
            ret.append(matches[0])
        track_length = tuple(ret)
    else:
        print("Lunghezza del tracciato: non presente.")
        
    return track_length

def parse_vehicle(record):
    check1 = lambda chk : 1 if(chk[1].contents[0].text.strip() == "Modified") else 0
    check2 = lambda chk: True if("Unplugged Performance" in chk) else False
    check3 = lambda chk: True if("Performance" in chk) else False

    index_vehicle = check1(record)
            
    try:    
        if(record[1].contents[index_vehicle].has_attr('href')):
            vehicle_href = record[1].contents[index_vehicle].get('href')
    except:
        vehicle_href = "Non presente"
            
    if(check2(record[1].contents[index_vehicle].text)):
        vehicle_name = re.sub("Unplugged Performance", "", record[1].contents[index_vehicle].text).strip()
    else:
        vehicle_name = record[1].contents[index_vehicle].text

    if(check3(record[1].contents[index_vehicle].text)):
        vehicle_name = re.sub("Performance", "", vehicle_name).strip()

    return (vehicle_name, vehicle_href)

def parse_track(record):
    raise  NotImplementedError

def parse_lap(record):
    raise NotImplementedError

def record_creator(laps, track):
    if(len(laps)>0):
        for lap in laps:
            vehicle_record = (lap['vehicle'], lap['vehicle_href'])
            track_record = list(track)
            track_record.append(lap['track_length'])
            track_record = tuple(track_record)
            lap_record = (change_laptime(lap['laptime']), lap['driver'], lap['ps_kg'], track[0], lap['vehicle'])
            db.insert_new_record(lap_record, track_record, vehicle_record)

def record_updater(vehicle):
    raise NotImplementedError

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
        new_track['name'] = track.contents[0].title()
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
    
    track_length = get_track_length(soup)

    tag = soup.find(class_=re.compile("table table-striped fl-laptimes-trackpage"))

    check_null = lambda chk : chk!=None
    laps_time = []

    if(check_null(tag)):
        laps = tag.findAll('tr')
        laps.pop(0)
        print("--Found " + str(len(laps)) + " laps, track " + track['name'] + " processed.")
        for lap in laps:
            lap_record = lap.findAll('td')

            vehicle = parse_vehicle(lap_record)
            new_lap = {
                'laptime': lap_record[3].contents[0].text,
                'driver': lap_record[2].contents[0].text,
                'track': track['name'],
                'track_length': track_length[0],
                'ps_kg': "".join(str(lap_record[4].contents[0]).split()),
                'vehicle_href': vehicle[1],
                'vehicle': vehicle[0]
            }
            print("----Laptime: " + str(new_lap))
            laps_time.append(new_lap)
    else:
        print("--Found 0 laps, track " + track['name'] + " not processed.")
    
    return laps_time