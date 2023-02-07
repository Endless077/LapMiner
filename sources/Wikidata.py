#  ____      ____ _____ ___  ____  _____ _______ ________ ______  _____      _       
# |_  _|    |_  _|_   _|_  ||_  _||_   _|_   __ |_   __  |_   _ `|_   _|    / \      
#   \ \  /\  / /   | |   | |_/ /    | |   | |__) || |_ \_| | | `. \| |     / _ \     
#    \ \/  \/ /    | |   |  __'.    | |   |  ___/ |  _| _  | |  | || |    / ___ \    
#     \  /\  /    _| |_ _| |  \ \_ _| |_ _| |_   _| |__/ |_| |_.' _| |_ _/ /   \ \_  
#      \/  \/    |_____|____||____|_____|_____| |________|______.|_____|____| |____| 

# IMPORT
import utils
import wikipediaapi

from bs4 import BeautifulSoup
from Interface.Source import Source

class Wikidata(Source):

    def __init__(self):
        pass

    def get_specs(self, vehicle: str, url: str, attr: set):
        
        specs = dict()

        response = utils.request(url, 10)

        if(response.status_code == 200):
            soup = BeautifulSoup(response.text, 'html.parser')       

            if("Layout" in attr):
                specs["Layout"] = self.get_layout()
            if("Dimensions" in attr):
                specs["Dimensions"] = self.get_dimensions()
            if("Engine" in attr):
                specs["Engine"] = self.get_engine()
            if("Trasmission" in attr):
                specs["Trasmission"] = self.get_trasmission()
            if("Performance" in attr):
                specs["Performance"] = self.get_performance()
            if("Overview" in attr):
                specs["Overview"] = self.get_overview()

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
        raise NotImplementedError
