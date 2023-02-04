#  _____  _____ _____  _________ _____ ____    ____      _    _________ ________  ______  _______ ________   ______  ______   
# |_   _||_   _|_   _||  _   _  |_   _|_   \  /   _|    / \  |  _   _  |_   __  .' ____ \|_   __ |_   __  |.' ___  .' ____ \  
#   | |    | |   | |  |_/ | | \_| | |   |   \/   |     / _ \ |_/ | | \_| | |_ \_| (___ \_| | |__) || |_ \_/ .'   \_| (___ \_| 
#   | '    ' |   | |   _  | |     | |   | |\  /| |    / ___ \    | |     |  _| _ _.____`.  |  ___/ |  _| _| |       _.____`.  
#    \ \__/ /   _| |__/ |_| |_   _| |_ _| |_\/_| |_ _/ /   \ \_ _| |_   _| |__/ | \____) |_| |_   _| |__/ \ `.___.'| \____) | 
#     `.__.'   |________|_____| |_____|_____||_____|____| |____|_____| |________|\______.|_____| |________|`.____ .'\______.' 

# IMPORT
import requests
from bs4 import BeautifulSoup
from random_user_agent.user_agent import UserAgent

HEADERS = {
    'User-Agent': 'user-agent',
    "Content-Type": "text/html"
    # other headers allowed.
}

def get_specs(user_agent: UserAgent, vehicle: str, url: str, attr: set):
    
    if not url.endswith(".html"):
        raise SystemError("This ultimatespecs page is not a specs page (specs page should ends with .html).")

    specs = dict()

    try:
        HEADERS["User-Agent"] = user_agent
        response = requests.get(url, headers=HEADERS, timeout=10)
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
        soup = BeautifulSoup(response.text, 'html.parser')

        if("Layout" in attr):
            specs["Layout"] = get_layout(soup)
        if("Dimensions" in attr):
            specs["Dimensions"] = get_dimensions(soup)
        if("Engine" in attr):
            specs["Engine"] = get_engine(soup)
        if("Trasmission" in attr):
            specs["Trasmission"] = get_trasmission(soup)
        if("Performance" in attr):
            specs["Performance"] = get_performance(soup)
        if("Overview" in attr):
            specs["Overview"] = get_overview(soup)

    return specs
    
def get_layout():
    raise NotImplementedError

def get_dimensions():
    raise NotImplementedError

def get_engine():
    raise NotImplementedError

def get_trasmission():
    raise NotImplementedError

def get_performance():
    raise NotImplementedError

def get_overview():
    return None

# Defination MAIN
def main():
    print("Hello World!")
    
# Definition NAME
if __name__ == "__main__":
    main()