#    ______  _____          _       ______    ______   
#  .' ___  ||_   _|        / \    .' ____ \ .' ____ \  
# / .'   \_|  | |         / _ \   | (___ \_|| (___ \_| 
# | |         | |   _    / ___ \   _.____`.  _.____`.  
# \ `.___.'\ _| |__/ | _/ /   \ \_| \____) || \____) | 
#  `.____ .'|________||____| |____|\______.' \______.' 

from typing import *
from dataclasses import dataclass

@dataclass
class LapTime:
    # Init function (classic)
    def __init__(self, lap_id: int, lap_time: float, driver: str, track: dict, vehicle: dict):
        # local variables
        self.__lap_id = lap_id
        self.__lap_time = lap_time
        self.__driver = driver

        # external variables
        self.__track = Track(track)
        self.__vehicle = Vehicle(vehicle)

    # String function
    def __str__(self):
        return f"Lap n° {self.__lap_id}:\n --Lap Time: {self.__lap_time}\n --Driver: {self.__driver}\n --Track: {self.__track.track_name}\n --Vehicle: {self.__vehicle.vehicle_name}."

    # Getter and Setter
    @property
    def lap_id(self):
        return self.__lap_id
    @lap_id.setter
    def lap_id(self, value):
        self.__lap_id = value

    @property
    def lap_time(self):
        return self.__lap_time
    @lap_time.setter
    def lap_time(self, value):
        self.__lap_time = value

    @property
    def driver(self):
        return self.__driver
    @driver.setter
    def driver(self, value):
        self.__driver = value

    @property
    def track(self):
        return self.__track
    @track.setter
    def track(self, value):
        self.__track = value

    @property
    def vehicle(self):
        return self.__vehicle
    @vehicle.setter
    def vehicle(self, value):
        self._vehicle = value

@dataclass
class Track:
    
    # Init function (classic)
    def __init__(self, track_id: int, track_name: str, country: str, total_length: float, laps: List[LapTime]) -> None:
        # local variables
        self.__track_id = track_id
        self.__track_name = track_name
        self.__country = country
        self.__total_length = total_length

        # external variables
        self.__track_laps = laps

    # Init function (with dict)
    def __init__(self, track: dict) -> None:
        # local variables
        self.__track_id = track["id"]
        self.__track_name = track["name"]
        self.__country = track["country"]
        self.__total_length = track["total_length"]

        # external variables
        self.__track_laps = track["laps"]

    # String function
    def __str__(self):
        return f"Track n° {self.__track_id}:\n --Circuit: {self.__track_name}\n --Country: {self.__country}\n --Total Length (km): {self.__total_length}."

    # Getter and Setter
    @property
    def track_id(self):
        return self.__track_id
    @track_id.setter
    def track_id(self, value):
        self.__track_id = value
    
    @property
    def track_name(self):
        return self.__track_name
    @track_name.setter
    def track_name(self, value):
        self.__track_name = value
    
    @property
    def country(self):
        return self.__country
    @country.setter
    def lap_id(self, value):
        self.__country = value
        
    @property
    def total_length(self):
        return self.__total_length
    @lap_id.setter
    def total_length(self, value):
        self.__total_length = value
    
    @property
    def laps(self):
        return self.__laps
    @lap_id.setter
    def lap_id(self, value):
        self.__laps = value

@dataclass
class Vehicle:

    # Init function (classic)
    def __init__(self, vehicle_id: int, vehicle_name: str, class_type: str, laps: List[LapTime]):
        # local variables
        self.__vehicle_id = vehicle_id
        self.__vehicle_name = vehicle_name
        self.__type = class_type

        # external variables
        self.__laps = laps
    
    # Init function (with dict)
    def __init__(self, vehicle: dict) -> None:
        # local variables
        self.__vehicle_id = vehicle["id"]
        self.__vehicle_name = vehicle["name"]
        self.__type = vehicle["class_type"]

        # external variables
        self.__laps = vehicle["laps"]

    # String function
    def __str__(self):
        return f"Vehicle n° {self.__vehicle_id}:\n --Name: {self.__vehicle_name}\n --Type: {self.__type}."

    # Getter and Setter
    @property
    def vehicle_id(self):
        return self.__vehicle_id
    @vehicle_id.setter
    def vehicle_id(self, value):
        self.vehicle_id = value
    
    @property
    def vehicle_name(self):
        return self.__vehicle_name
    @vehicle_name.setter
    def vehicle_name(self, value):
        self.__vehicle_name = value
    
    @property
    def type(self):
        return self.__type
    @type.setter
    def type(self, value):
        self.__type = value
        
    @property
    def laps(self):
        return self.__laps
    @laps.setter
    def laps(self, value):
        self.__laps = value

#################################

@dataclass
class Car(Vehicle):
    # Init function (classic)
    def __init__(self, vehicle_id: int, vehicle_name: str, class_type: str, laps: List[LapTime],
                layout: dict, dimensions: dict, engine: dict,
                trasmission: dict, performance: dict, overview: dict):
        
        if class_type != "Car":
            raise ValueError("Error, this vehicle is not a car.")
        
        # local variables
        super().__init__(vehicle_id, vehicle_name, class_type, laps)

        # external variables
        self.__layout = Layout(layout)
        self.__dimensions = Dimensions(dimensions)
        self.__engine = Engine(engine)
        self.__trasmission = Trasmission(trasmission)
        self.__performance = Performance(performance)
        self.__overview = Overview(overview)
    
    # Init function (with dict)
    def __init__(self, vehicle: dict) -> None:

        if vehicle["class_type"] != "Car":
            raise ValueError("Error, this vehicle is not a car.")

        # local variables
        super().__init__(vehicle)

        # external variables
        self.__layout = vehicle["layout"]
        self.__dimensions = vehicle["dimensions"]
        self.__engine = vehicle["engine"]
        self.__trasmission = vehicle["trasmission"]
        self.__performance = vehicle["performance"]
        self.__overview = vehicle["overview"]

    # String function
    def __str__(self):
        return f"Car n° {self.__vehicle_id}:\n --Name: {self.__vehicle_name}\n --Other info: <info>."

    # Getter and Setter
    @property
    def layout(self):
        return self.__layout
    @layout.setter
    def layout(self, value):
        self.__layout = value
    
    @property
    def dimensions(self):
        return self.__dimensions
    @dimensions.setter
    def dimensions(self, value):
        self.__dimensions = value
    
    @property
    def engine(self):
        return self.__engine
    @engine.setter
    def engine(self, value):
        self.__engine = value
        
    @property
    def trasmission(self):
        return self.__trasmission
    @trasmission.setter
    def trasmission(self, value):
        self.__trasmission = value
    
    @property
    def performance(self):
        return self.__performance
    @performance.setter
    def performance(self, value):
        self.__performance = value

    @property
    def overview(self):
        return self.__overview
    @overview.setter
    def overview(self, value):
        self.__overview = value

@dataclass
class Motorcycle(Vehicle):
    
    # Init function (don't exist)
    def __init__(self, *args) -> None:
        raise NotImplementedError

#################################

@dataclass
class Layout:

    # Init function (classic)
    def __init__(self):
        pass
    
    # String function
    def __str__(self):
        pass

@dataclass
class Dimensions:
    # Init function (classic)
    def __init__(self):
        pass
    
    # String function
    def __str__(self):
        pass

@dataclass
class Engine:
    # Init function (classic)
    def __init__(self):
        pass
    
    # String function
    def __str__(self):
        pass
@dataclass
class Trasmission:
    # Init function (classic)
    def __init__(self):
        pass
    
    # String function
    def __str__(self):
        pass

@dataclass
class Performance:
    # Init function (classic)
    def __init__(self):
        pass
    
    # String function
    def __str__(self):
        pass

@dataclass
class Overview:
    # Init function (classic)
    def __init__(self):
        pass
    
    # String function
    def __str__(self):
        pass