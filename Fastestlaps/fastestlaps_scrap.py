# Fastestlaps scrap

import requests
import re
import fastestlaps_db as db
from bs4 import BeautifulSoup

LINK = "https://fastestlaps.com/tracks"
BASE_LINK = "https://fastestlaps.com"
HEADERS = {
    'User-Agent': 'user-agent',
    "Content-Type": "text/html"
    # other headers allowed.
}

def change_laptime(laptime):
    # Change a laptime "mm:ss.ms" in seconds
    # :param laptime: a string.
    # :return: laptime converted in seconds or 0.

    check = re.compile('^\d*:\d*\.\d*$')
    res = [substr for substr in laptime.split() if check.match(substr)]
    if(len(res)>0):
        m, s = res[0].split(':')
        return round(int(m) * 60 + float(s), 2)
    else:
        print("Impossible parsing laptime.")
        return "Non presente."

def clean_record(record):
    new_line_count = record.contents.count('\n')
    for value in range(new_line_count):
        record.contents.remove('\n')

def extract_specs(specs):
    # Get a specific vehicle specs attribute
    # :param specs: a given vehicle specs dict.
    # :return: attribute value or None.

    raise NotImplementedError

def info_attr(soup, attribute):
    # Get a specific INFO attrbute
    # :param soup: a html page.
    # :param attribute: a specific fastestlap INFO attribute.
    # :return: attribute value or None.

    print("Getting " + attribute + "...")
    tag = soup.find(class_=re.compile("table fl-datasheet"))
    table = tag.findAll('tr')

    attr = None

    for record in table:
        new_line_count = record.contents.count('\n')
        for value in range(new_line_count):
            record.contents.remove('\n')

        if(record.contents[0].text == attribute):
            attr = record.contents[1].text
            break

    return attr

def get_track_country(value):
    # Extract the correct value from a specific scrap country value
    # :param value: a scrap value.
    # :return: the extract country or "Non Presente"".

    country = "Non Presente"

    if(value!=None):
        country = value.strip().title()
    else:
        print("Impossible parsing track length.")
        
    return country

def get_track_length(value):
    # Extract the correct value from a specific scrap length value
    # :param value: a scrap value.
    # :return: (km_length, miles_length) or (Non Presente, Non Presente).

    track_length = ("Non Presente", "Non Presente")

    if(value!=None):
        all_length = value.split('/')
        return_value = []
        match = re.compile('[+-]?\d+\.\d+')
        for length in all_length:
            matches = re.findall(match, length.strip())
            return_value.append(matches[0])
        track_length = tuple(return_value)
    else:
        print("Impossible parsing track length.")
        
    return track_length

def parse_vehicle(record):
    # Extract the correct value from a specific scrap length value
    # :param record: a record value from html page.
    # :return: (vehicle_name, vehicle_href) or corrispective default value.

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

def record_creator(laps, track_record):
    # Get all track info (i.e Country, length and laps), ignore track if it haven't laptime
    # :param laps: a given laps dict list with some info (laptime, driver, track, ps_kg, vehicle_href, vehicle).
    # :param track_record: a given track tuple with some info (name, href, country, length).
    # :return:

    if(len(laps)>0):
        for lap in laps:
            vehicle_record = (lap['vehicle'], lap['vehicle_href'])
            lap_record = (change_laptime(lap['laptime']), lap['driver'], lap['ps_kg'], track_record[0], lap['vehicle'])
            db.insert_new_record(lap_record, track_record, vehicle_record)

def record_updater():
    raise NotImplementedError

def get_all_tracks(user_agent):
    # Get all tracks from the main track page of fastestlaps.com
    # :param user-agent: a user agent random string.
    # :return: a list of all track dict (name, href).

    try:
        HEADERS["User-Agent"] = user_agent
        response = requests.get(LINK, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.ConnectionError as e:
        print("Error (connection):")
        print(e)
    except requests.Timeout as e:
        print("Error (timeout):")
        print(e)
    except requests.HTTPError as e:
        print("Error (http):")
        print(e)
    except:
            print("Someting goes wrong here.")
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

def get_track_info(user_agent, track):
    # Get all track info (i.e Country, length and laps), ignore track if it haven't laptime
    # :param user-agent: a user agent random string.
    # :param track: a dict with two keys (name and href).
    # :return: a dict with two keys (laps_time that is a list and track_info that is a tuple).

    track_link = BASE_LINK + track['href']

    try:
        HEADERS["User-Agent"] = user_agent
        response = requests.get(track_link, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.ConnectionError as e:
        print("Error (connection):")
        print(e)
    except requests.Timeout as e:
        print("Error (timeout):")
        print(e)
    except requests.HTTPError as e:
        print("Error (http):")
        print(e)
    except:
            print("Someting goes wrong here.")
    else:
        print("HTTP Status request: " + str(response.status_code))

    print("Parsing html...")
    soup = BeautifulSoup(response.text, 'html.parser')
    
    track_country = get_track_country(info_attr(soup, "Country"))
    track_length = get_track_length(info_attr(soup, "Track length"))

    track_info = (track_country, track_length)

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
                'ps_kg': "".join(str(lap_record[4].contents[0]).split()),
                'vehicle_href': vehicle[1],
                'vehicle': vehicle[0]
            }
            print("----Laptime: " + str(new_lap))

            laps_time.append(new_lap)
    else:
        print("--Found 0 laps, track " + track['name'] + " not processed.")
    
    ret = {'laps_time': laps_time, 'track_info': track_info}
    return ret

def get_vehicle_info(user_agent, vehicle):
    # Get all vheicle info (i.e Country, engine, pwer....), ignore if value don't exist
    # :param user-agent: a user agent random string.
    # :param vheicle: a dict with two keys (name and href).
    # :return: a dict with a lot of keys (key = attribute).

    vehicle_link = BASE_LINK + vehicle[1]

    try:
        HEADERS["User-Agent"] = user_agent
        response = requests.get(vehicle_link, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.ConnectionError as e:
        print("Error (connection):")
        print(e)
    except requests.Timeout as e:
        print("Error (timeout):")
        print(e)
    except requests.HTTPError as e:
        print("Error (http):")
        print(e)
    except:
            print("Someting goes wrong here.")
    else:
        print("HTTP Status request: " + str(response.status_code))

    vehicle_record = {'name': vehicle[0]}
    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.findAll(class_=re.compile("table fl-datasheet"))

    for table in tables:
        rows = table.findAll('tr')
        for record in rows:
            clean_record(record)
            key = record.contents[0].text.strip()
            value = record.contents[1].text.strip()
            vehicle_record[key] = value

    return vehicle_record