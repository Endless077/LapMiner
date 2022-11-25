# Utils

import requests
import time
import os
import sys
import re
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import HardwareType, SoftwareEngine, SoftwareName, SoftwareType, OperatingSystem, Popularity

def random_user_agent():
    user_agent_rotator = None

    hardwareTypes =         [HardwareType.COMPUTER.value, HardwareType.MOBILE.value]
    softwareEngines =       [SoftwareEngine.GECKO.value, SoftwareEngine.BLINK.value, SoftwareEngine.WEBKIT.value] 
    softwareNames =         [SoftwareName.EDGE.value, SoftwareName.FIREFOX.value, SoftwareName.CHROME.value, SoftwareName.BRAVE.value]
    softwareTypes =         [SoftwareType.APPLICATION.value]
    operatingSystems =      [OperatingSystem.LINUX.value, OperatingSystem.IOS.value, OperatingSystem.ANDROID.value, OperatingSystem.WINDOWS.value]
    popularity_services =   [Popularity.UNCOMMON.value, Popularity.COMMON.value, Popularity.POPULAR.value, Popularity.AVERAGE.value]

    user_agent_rotator = UserAgent(hardware_type=hardwareTypes, operating_system=operatingSystems, software_type=softwareTypes,
                                software_name=softwareNames, software_engine=softwareEngines, popularity=popularity_services,
                                limit=100)

    return user_agent_rotator

def html_downloader():
    LINK = []
    HEADERS = {
    'User-Agent': 'user-agent',
    "Content-Type": "text/html"
    # other headers allowed.
    }

    user_agent_generator = random_user_agent()

    for site in LINK:
        try:
            HEADERS["User-Agent"] = user_agent_generator.get_random_user_agent()
            response = requests.get(site, headers=HEADERS, timeout=10)
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
            
            if not os.path.exists("./Temp"):
                os.mkdir("./Temp")
            path = "./Temp/" + site + ".html"
            with open(path, 'x') as f:
                f.write(response.text)

def request(link, headers, timeout):
    try:
        response = requests.get(link, headers=headers, timeout=timeout)
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
    
    return response