#    ______      _      _______    ______      ______       _    _________    _       
#  .' ___  |    / \    |_   __ \ .' ____ \    |_   _ `.    / \  |  _   _  |  / \      
# / .'   \_|   / _ \     | |__) || (___ \_______| | `. \  / _ \ |_/ | | \_| / _ \     
# | |         / ___ \    |  __ /  _.____`|______| |  | | / ___ \    | |    / ___ \    
# \ `.___.'\_/ /   \ \_ _| |  \ \| \____) |    _| |_.' _/ /   \ \_ _| |_ _/ /   \ \_  
#  `.____ .|____| |____|____| |___\______.'   |______.|____| |____|_____|____| |____|

# IMPORT
import re
from bs4 import BeautifulSoup
from Interface.Source import Source

import utils
class CarsData(Source):

    def __init__(self):
        pass
    
    def get_specs(self, url: str, attr: set):
        
        cars_data_category = ["tech","sizes","options"]
        specs = dict()

        response = utils.request(url, 10)

        if(response.status_code == 200):
            specs_map = dict()

            if url[-1] == "/":
                url = url[:-1]

            for category in cars_data_category:
                curr_url = f"{url}/{category}"
                intestazione_dict = {}

                response = utils.request(curr_url, 10)
                if(response.status_code == 200):
                    page = BeautifulSoup(response.text, 'html.parser')
                    tables = page.find_all('table', {'width': '100%', 'style': 'font-size:16px;'})
                    for table in tables:
                        rows = table.find_all('tr')[1:]
                        for row in rows:
                            cells = row.find_all('td')
                            if len(cells) == 2:
                                intestazione = cells[0].text.replace(":","").strip()
                                dato = cells[1].text.strip()
                                if ((len(intestazione) > 0) and (len(dato) > 0 and not re.search(r"^n/a",dato))):
                                    intestazione_dict[intestazione] = dato
                                    specs_map[category] = intestazione_dict

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
        layout_specs = dict()
        
        # Engine Layout non allowed.

        if("Drive Wheel" in specs_map["tech"].keys()):
            if("front" in specs_map["tech"]["Drive Wheel"].lower()):
                layout_specs["wheel_drive"] = "Front"
            elif("rear" in specs_map["Drive Wheel"].lower()):
                layout_specs["wheel_drive"] = "Rear"
            elif("front+rear" in specs_map["Drive Wheel"].lower()):
                layout_specs["wheel_drive"] = "All"

        
        # Class Type not allowed

        return layout_specs

    def get_dimensions(self, specs_map: dict):
        dimensions_specs = dict()

        if("Curb Weight" in specs_map["sizes"].keys()):
            match = re.compile('(\d+) *[Kk]+[Gg]+.*')
            result = match.findall(specs_map["sizes"]["Curb Weight"])
            if(len(result) > 0):
                dimensions_specs["curb_weight"] = round(float(result[0]), 2)
        
        match = re.compile('(\d+) *[Mm]+[Mm]+.*')
        
        if("Wheelbase" in specs_map["sizes"].keys()):
            result = match.findall(specs_map["sizes"]["Wheelbase"])
            if(len(result) > 0):
                mm_result = float(result[0])/1000
                dimensions_specs["wheelbase"] = round(mm_result, 2)

        if("Length" in specs_map["sizes"].keys()):
            result = match.findall(specs_map["sizes"]["Length"])
            if(len(result) > 0):
                mm_result = float(result[0])/1000
                dimensions_specs["length"] = round(mm_result, 2)

        if("Width" in specs_map["sizes"].keys()):
            result = match.findall(specs_map["sizes"]["Width"])
            if(len(result) > 0):
                mm_result = float(result[0])/1000
                dimensions_specs["width"] = round(mm_result, 2)
           
        if("Height" in specs_map["sizes"].keys()):
            result = match.findall(specs_map["sizes"]["Height"])
            if(len(result) > 0):
                mm_result = float(result[0])/1000
                dimensions_specs["height"] = round(mm_result, 2)

        return dimensions_specs
    
    def get_engine(self, specs_map: dict):
        engine_specs = dict()
        
        if("Cylinders" in specs_map["tech"].keys()):
            engine_specs["engine_name"] = specs_map["tech"]["Cylinders"]

        # Displacement not allowed.

        if("Total Max. Power (kW)" in specs_map["tech"].keys()):
            convert = float(specs_map["tech"]["Total Max. Power (kW)"])*1.34102209
            engine_specs["power"] = round(convert,2)
        elif("Total Max. Power (hp)" in specs_map["tech"].keys()):
            convert = float(specs_map["tech"]["Total Max. Power (hp)"])*1.014
            engine_specs["power"] = round(convert,2)
        
        if("Max Torque" in specs_map["tech"].keys()):
            match = re.compile('(\d+) *[Nn]+[Mm]+.*')
            result = match.findall(specs_map["tech"]["Max Torque"])
            if(len(result) > 0):
                engine_specs["torque"] = int(result[0])

        return engine_specs

    def get_trasmission(self, specs_map: dict):
        trasmission_specs = dict()

        if("Transmission" in specs_map["tech"].keys()):
            trasmission_specs["trasmission_name"] = specs_map["tech"]["Transmission"]
            type_list = ["manual", "automatic", "semi-automatic", "semi automatic", "semiautomatic", "dual-clutch", "dual clutch", "dualclutch", "sequential"]
            type_index = [int(specs_map["tech"]["Transmission"].lower().find(type_value)) for type_value in type_list]
            occurrences = [value for value in type_index if value > 0]
            if(len(occurrences) > 0):
                trasmission_specs["trasmission_type"] = type_list[type_index.index(min(occurrences))].replace(" ","-").title()
                if(trasmission_specs["trasmission_type"] == "Dualclutch"):
                    trasmission_specs["trasmission_type"] = "Dual Clutch"
                elif(trasmission_specs["trasmission_type"] == "Semiautomatic"):
                    trasmission_specs["trasmission_type"] = "Semi Automatic"

            trasmission_specs["n_trasmission"] = int(re.search(r'\d+', specs_map["tech"]["Transmission"]).group())


        return trasmission_specs
    
    def get_performance(self, specs_map: dict):
        performance_specs = dict()

        if("Top Speed" in specs_map["tech"].keys()):
            match = re.compile('(\d+) *[Kk]+[Mm]+[/]+[Hh]+.*')
            result = match.findall(specs_map["tech"]["Top Speed"])
            if(len(result) > 0):
                performance_specs["top_speed"] = round(float(result[0]), 2)
           
        if("Acceleration 0-100 Km / H" in specs_map["tech"].keys()):
            match = re.compile('(\d+,{0,1}\d{0,}) *[Ss]+.*')
            result = match.findall(specs_map["tech"]["Acceleration 0-100 Km / H"])
            if(len(result) > 0):
                performance_specs["accelleration"] = round(float(result[0].replace(",",".")), 2)

        # Break Distance not allowed.S

        return performance_specs
