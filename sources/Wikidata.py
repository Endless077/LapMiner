#  ____      ____ _____ ___  ____  _____ _______ ________ ______  _____      _       
# |_  _|    |_  _|_   _|_  ||_  _||_   _|_   __ |_   __  |_   _ `|_   _|    / \      
#   \ \  /\  / /   | |   | |_/ /    | |   | |__) || |_ \_| | | `. \| |     / _ \     
#    \ \/  \/ /    | |   |  __'.    | |   |  ___/ |  _| _  | |  | || |    / ___ \    
#     \  /\  /    _| |_ _| |  \ \_ _| |_ _| |_   _| |__/ |_| |_.' _| |_ _/ /   \ \_  
#      \/  \/    |_____|____||____|_____|_____| |________|______.|_____|____| |____| 

# IMPORT
import re
from bs4 import BeautifulSoup
from Interface.Source import Source

import wikipediaapi
import urllib.parse
import utils
class Wikidata(Source):

    def __init__(self):
        pass

    def get_specs(self, url: str, attr: set):

        wiki = wikipediaapi.Wikipedia(
                language='en',
                extract_format=wikipediaapi.ExtractFormat.WIKI
        )

        specs = dict()

        match = re.search(r"https://en.wikipedia.org/wiki/(.*)", url)

        if match:
            page_name = match.group(1)
            page_name = urllib.parse.unquote_plus(page_name)
            page_name = page_name.encode("utf-8")
            page_name = urllib.parse.unquote_to_bytes(page_name).decode("utf-8")
            page = wiki.page(page_name)

            if page.exists():
                soup = BeautifulSoup(utils.requests(page.fullurl,10).text, 'html.parser')
                infobox_table = soup.find('table', class_='infobox hproduct')
                
                if infobox_table:
                    specs_map = dict()
                    for row in infobox_table.find_all('tr'):
                        intestazione = row.th
                        dato = row.td
                        if(intestazione and dato):
                            specs_map[intestazione.text.strip()] = dato.text.strip()
                else:
                    ValueError("Infobox table not found.")
            else:
                SyntaxError("The wikipedia page don't exist.")
        else:
            SyntaxError("The given url is not a valid wikipedia english page.")

        specs["Vehicle"] = None
        
        if("Layout" in attr):
            specs["Layout"] = self.get_layout(specs_map)
        if("Dimensions" in attr):
            specs["Dimensions"] = self.get_dimensions(specs_map)
        if("Engine" in attr):
            specs["Engine"] = self.get_engine(specs_map)
        if("Trasmission" in attr):
            specs["Trasmission"] = self.get_trasmission(specs_map)
        if("Performance" in attr):
            specs["Performance"] = self.get_performance(specs_map)
            
        return specs
    
    def get_layout(self, specs_map: dict):
        raise NotImplementedError

    def get_dimensions(self, specs_map: dict):
        raise NotImplementedError
        
    def get_engine(self, specs_map: dict):
        raise NotImplementedError

    def get_trasmission(self, specs_map: dict):
        raise NotImplementedError

    def get_performance(self, specs_map: dict):
        raise NotImplementedError
