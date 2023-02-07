#  _____  _____ _____  _________ _____ ____    ____      _    _________ ________  ______  _______ ________   ______  ______   
# |_   _||_   _|_   _||  _   _  |_   _|_   \  /   _|    / \  |  _   _  |_   __  .' ____ \|_   __ |_   __  |.' ___  .' ____ \  
#   | |    | |   | |  |_/ | | \_| | |   |   \/   |     / _ \ |_/ | | \_| | |_ \_| (___ \_| | |__) || |_ \_/ .'   \_| (___ \_| 
#   | '    ' |   | |   _  | |     | |   | |\  /| |    / ___ \    | |     |  _| _ _.____`.  |  ___/ |  _| _| |       _.____`.  
#    \ \__/ /   _| |__/ |_| |_   _| |_ _| |_\/_| |_ _/ /   \ \_ _| |_   _| |__/ | \____) |_| |_   _| |__/ \ `.___.'| \____) | 
#     `.__.'   |________|_____| |_____|_____||_____|____| |____|_____| |________|\______.|_____| |________|`.____ .'\______.' 

# IMPORT
import re
import requests
from bs4 import BeautifulSoup
from Interface.Source import Source

import utils

class UltimateSpecs(Source):

    def __init__(self):
        pass

    def get_specs(self, vehicle: str, url: str, attr: set):
        
        if not url.endswith(".html"):
            raise SystemError("This ultimatespecs page is not a specs page (specs page should ends with .html).")

        specs = dict()

        response = utils.request(url, 10)

        if(response.status_code == 200):
            soup = BeautifulSoup(response.text, 'html.parser')

            tds = soup.find_all("td", class_="tabletd", align="right")
            new_line = "\n"

            specs_map = dict()

            for td in tds:
                intestazione = td.text.replace(':','').strip()
                dato = td.find_next_sibling('td').text.replace(new_line,'').strip()

                if ((len(intestazione) > 0) and (len(dato) > 0 and not re.search(r"^-",dato))):
                    specs_map[intestazione] = dato        

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
            if("Overview" in attr):
                specs["Overview"] = self.get_overview(specs_map)

        return specs
    
    def get_layout(specs_map: dict):
        layout_specs = dict()

        if("Engine Position" in specs_map.keys()):
            if("front" in specs_map["Engine Position"].lower()):
                layout_specs["engine_layout"] = "Front"
            elif("mid" in specs_map["Engine Position"].lower()):
                layout_specs["engine_layout"] = "Middle"
            elif("rear" in specs_map["Engine Position"].lower()):
                layout_specs["engine_layout"] = "Rear"
        
        if("Drive wheels - Traction - Drivetrain" in specs_map.keys()):
            if("fwd" in specs_map["Drive wheels - Traction - Drivetrain"].lower()):
                layout_specs["wheel_drive"] = "Front"
            elif("rwd" in specs_map["Drive wheels - Traction - Drivetrain"].lower()):
                layout_specs["wheel_drive"] = "Rear"
            elif("awd" in specs_map["Drive wheels - Traction - Drivetrain"].lower()):
                layout_specs["wheel_drive"] = "All"

        # Class Type not allowed
        
        return layout_specs

    def get_dimensions(specs_map: dict):
        dimensions_specs = dict()

        if("Curb Weight" in specs_map.keys()):
            match_kg = re.compile('(\d+) *[Kk]+[Gg]+.*')
            result = match_kg.findall(specs_map["Curb Weight"])
            if(len(result) > 0):
                dimensions_specs["curb_weight"] = round(float(result[0]), 2)
            else:
                match_lbs = re.compile('(\d+) *[Ll]+[Bb]+[Ss]+.*')
                result = match_lbs.findall(specs_map["Curb Weight"])
                if(len(result) > 0):
                    lbs_result = float(result[0])*0.45359237
                    dimensions_specs["curb_weight"] = round(lbs_result,2)

        match_cm = re.compile('(\d+) *[Cc]+[Mm]+.*')
        match_in = re.compile('(\d+) *[Ii]+[Nn]+.*')

        if("Wheelbase" in specs_map.keys()):
            result = match_cm.findall(specs_map["Wheelbase"])
            if(len(result) > 0):
                cm_result = float(result[0])/100
                dimensions_specs["wheelbase"] = round(cm_result, 2)
            else:
                result = match_in.findall(specs_map["Wheelbase"])
                if(len(result) > 0):
                    in_result = float(result[0])*0.0254
                    dimensions_specs["wheelbase"] = round(in_result,2)

        if("Length" in specs_map.keys()):
            result = match_cm.findall(specs_map["Length"])
            if(len(result) > 0):
                cm_result = float(result[0])/100
                dimensions_specs["long"] = round(cm_result, 2)
            else:
                result = match_in.findall(specs_map["Length"])
                if(len(result) > 0):
                    in_result = float(result[0])*0.0254
                    dimensions_specs["long"] = round(in_result,2)

        if("Width" in specs_map.keys()):
            result = match_cm.findall(specs_map["Width"])
            if(len(result) > 0):
                cm_result = float(result[0])/100
                dimensions_specs["wide"] = round(cm_result, 2)
            else:
                result = match_in.findall(specs_map["Width"])
                if(len(result) > 0):
                    in_result = float(result[0])*0.0254
                    dimensions_specs["wide"] = round(in_result,2)

        if("Height" in specs_map.keys()):
            result = match_cm.findall(specs_map["Height"])
            if(len(result) > 0):
                cm_result = float(result[0])/100
                dimensions_specs["high"] = round(cm_result, 2)
            else:
                result = match_in.findall(specs_map["Height"])
                if(len(result) > 0):
                    in_result = float(result[0])*0.0254
                    dimensions_specs["high"] = round(in_result,2)

        return dimensions_specs
    
    def get_engine(specs_map: dict):
        engine_specs = dict()
        
        if("Engine type - Number of cylinders" in specs_map.keys()):
             engine_specs["engine_type"] = specs_map["Engine type - Number of cylinders"]

        # Displacement not allowed.

        if("Maximum power - Output - Horsepower" in specs_map.keys()):
            match_ps = re.compile('(\d+) *[Pp]+[Ss]+.*')
            result = match_ps.findall(specs_map["Maximum power - Output - Horsepower"])
            if(len(result) > 0):
                engine_specs["power"] = int(result[0])
            else:
                match_bhp = re.compile('(\d+) *[Hh]+[Pp]+.*')
                result = match_bhp.findall(specs_map["Maximum power - Output - Horsepower"])
                if(len(result) > 0):
                    bhp_result = float(result[0])*1.014
                    engine_specs["power"] = round(bhp_result,2)
                else:
                    match_kw = re.compile('(\d+) *[Kk]+[Ww]+.*')
                    result = match_kw.findall(specs_map["Maximum power - Output - Horsepower"])
                    if(len(result) > 0):
                        kw_result = float(result[0])*1.34102209
                        engine_specs["power"] = round(kw_result,2)

        if("Maximum torque" in specs_map.keys()):
            match_nm = re.compile('(\d+) *[Nn]+[Mm]+.*')
            result = match_nm.findall(specs_map["Maximum torque"])
            if(len(result) > 0):
                engine_specs["power"] = int(result[0])
            else:
                match_lbft = re.compile('(\d+) *[Ll]+[Bb]+[- ]+[Ff]+[Tt].*')
                result = match_lbft.findall(specs_map["Maximum torque"])
                if(len(result) > 0):
                    bhp_result = float(result[0])*1.014
                    engine_specs["power"] = round(bhp_result,2)
        
        return engine_specs

    def get_trasmission(specs_map: dict):
        trasmission_specs = dict()

        if("Transmission Gearbox - Number of speeds" in specs_map.keys()):
            trasmission_specs["trasmission_name"]
            type_list = ["manual", "automatic", "semi-automatic", "semi automatic", "semiautomatic", "dual-clutch", "dual clutch", "dualclutch", "sequential"]
            type_index = [int(specs_map["Transmission Gearbox - Number of speeds"].lower().find(type_value)) for type_value in type_list]
            occurrences = [value for value in type_index if value > 0]
            if(len(occurrences) > 0):
                trasmission_specs["trasmission_type"] = type_list[type_index.index(min(occurrences))].replace(" ","-").title()
                if(trasmission_specs["trasmission_type"] == "Dualclutch"):
                    trasmission_specs["trasmission_type"] = "Dual Clutch"
                elif(trasmission_specs["trasmission_type"] == "Semiautomatic"):
                    trasmission_specs["trasmission_type"] = "Semi Automatic"

            trasmission_specs["n_trasmission"] = int(re.search(r'\d+', specs_map["Transmission Gearbox - Number of speeds"]).group())

        return trasmission_specs
    
    def get_performance(specs_map: dict):
        performance_specs = dict()

        if("Top Speed" in specs_map.keys()):
            match_kph = re.compile('(\d+) *[Kk]+[Pp]+[Hh]+.*')
            result = match_kph.findall(specs_map["Top Speed"])
            if(len(result) > 0):
                performance_specs["top_speed"] = round(float(result[0]), 2)
            else:
                match_mph = re.compile('(\d+) *[Mm]+[Pp]+[Hh]+.*')
                result = match_mph.findall(specs_map["Top Speed"])
                if(len(result) > 0):
                    mph_result = float(result[0])*1.60934
                    performance_specs["top_speed"] = round(mph_result,2)

        if("Acceleration 0 to 100 km/h (0 to 62 mph)" in specs_map.keys()):
            match = re.compile('(\d+) *[Ss]++.*')
            result = match.findall(specs_map["Acceleration 0 to 100 km/h (0 to 62 mph)"])
            if(len(result) > 0):
                performance_specs["accelleration"] = round(float(result[0]), 2)
        # Break Distance not allowed.

        return performance_specs

    def get_overview():
        return None
