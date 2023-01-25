#    ______  _____          _       ______    ______   ________   ______   
#  .' ___  ||_   _|        / \    .' ____ \ .' ____ \ |_   __  |.' ____ \  
# / .'   \_|  | |         / _ \   | (___ \_|| (___ \_|  | |_ \_|| (___ \_| 
# | |         | |   _    / ___ \   _.____`.  _.____`.   |  _| _  _.____`.  
# \ `.___.'\ _| |__/ | _/ /   \ \_| \____) || \____) | _| |__/ || \____) | 
#  `.____ .'|________||____| |____|\______.' \______.'|________| \______.' 

from typing import *
from dataclasses import dataclass

#################################
@dataclass
class Layout:

    # Init function
    def __init__(self, layout_id: int, engine_layout: str, wheel_drive: str, class_type: str) -> None:
        self.__layout_id = layout_id
        self.__engine_layout = engine_layout
        self.__wheel_drive = wheel_drive
        self.__class_type = class_type
    
    # String function
    def __str__(self) -> str:
        return f"Engine n° {self.__layout_id}:\n --Layout: {self.__engine_layout}\n --Wheel Drive: {self.__wheel_drive}\n --Class Type: {self.__class_type}"

    # Getter and Setter
    @property
    def layout_id(self):
        return self.__layout_id
    @layout_id.setter
    def layout_id(self, value):
        self.__layout_id = value
    
    @property
    def engine_layout(self):
        return self.__engine_layout
    @engine_layout.setter
    def engine_layout(self, value):
        self.__engine_layout = value
    
    @property
    def wheel_drive(self):
        return self.__wheel_drive
    @wheel_drive.setter
    def wheel_drive(self, value):
        self.__wheel_drive = value
    
    @property
    def class_type(self):
        return self.__class_type
    @class_type.setter
    def class_type(self, value):
        self.__class_type = value

@dataclass
class Dimensions:

    # Init function
    def __init__(self, dim_id: int, curb_weight: float, wheelbase: float, long: float, high: float, wide: float):
        self.__dim_id = dim_id
        self.__curb_weight = curb_weight
        self.__wheelbase = wheelbase
        self.__long = long
        self.__high = high
        self.__wide = wide
    
    # String function
    def __str__(self) -> str:
        return f"Dimensions n° {self.__dim_id}:\n --Curb Weight: {self.__curb_weight}\n --Wheelbase: {self.__wheelbase}\n --Long: {self.__long}\n --High: {self.__high}\n --Wide: {self.__wide}"

    # Getter and Setter
    @property
    def dim_id(self):
        return self.__dim_id
    @dim_id.setter
    def dim_id(self, value):
        self.__dim_id = value

    @property
    def curb_weight(self):
        return self.__curb_weight
    @curb_weight.setter
    def curb_weight(self, value):
        self.__curb_weight = value

    @property
    def wheelbase(self):
        return self.__wheelbase
    @wheelbase.setter
    def wheelbase(self, value):
        self.__wheelbase = value
    
    @property
    def long(self):
        return self.__long
    @long.setter
    def long(self, value):
        self.__long = value

    @property
    def high(self):
        return self.__high
    @high.setter
    def high(self, value):
        self.__high = value

    @property
    def wide(self):
        return self.__wide
    @wide.setter
    def wide(self, value):
        self.__wide = value

@dataclass
class Engine:

    # Init function
    def __init__(self, engine_id: int, engine: str, displacement: float, power: int, torque: int):
        self.__engine_id = engine_id
        self.__engine = engine
        self.__displacement = displacement
        self.__power = power
        self.__torque = torque

    # String function
    def __str__(self) -> str:
        return f"Engine n° {self.__engine_id}:\n --Engine: {self.__engine}\n --Displacement: {self.__displacement}\n --Power: {self.__power}\n --Torque: {self.__torque}"

    # Getter and Setter
    @property
    def engine_id(self):
        return self.__engine_id
    @engine_id.setter
    def engine_id(self, value):
        self.__engine_id = value
    
    @property
    def engine(self):
        return self.__engine
    @engine.setter
    def engine(self, value):
        self.__engine = value
    
    @property
    def displacement(self):
        return self.__displacement
    @displacement.setter
    def displacement(self, value):
        self.__displacement = value
    
    @property
    def power(self):
        return self.__power
    @power.setter
    def power(self, value):
        self.__power = value
    
    @property
    def torque(self):
        return self.__torque
    @torque.setter
    def torque(self, value):
        self.__torque = value

@dataclass
class Trasmission:

    # Init function
    def __init__(self, trasmission_id: int, trasmission_name: str, trasmission_type: str, n_trasmission: int):
        self.__trasmission_id = trasmission_id
        self.__trasmission_name = trasmission_name
        self.__trasmission_type = trasmission_type
        self.__n_trasmission = n_trasmission
    
    # String function
    def __str__(self) -> str:
        return f"Trasmission n° {self.__trasmission_id}:\n --Trasmission Name: {self.__trasmission_name}\n --Trasmission Type: {self.__trasmission_type}\n --N° Trasmission: {self.__n_trasmission}"

    # Getter and Setter
    @property
    def trasmission_id(self):
        return self.__trasmission_id
    @trasmission_id.setter
    def trasmission_id(self, value):
        self.__trasmission_id = value

    @property
    def trasmission_name(self):
        return self.__trasmission_name
    @trasmission_name.setter
    def trasmission_name(self, value):
        self.__trasmission_name = value

    @property
    def trasmission_type(self):
        return self.__trasmission_type
    @trasmission_type.setter
    def trasmission_type(self, value):
        self.__trasmission_type = value
    
    @property
    def n_trasmission(self):
        return self.__n_trasmission
    @n_trasmission.setter
    def n_trasmission(self, value):
        self.__n_trasmission = value 

@dataclass
class Performance:

    # Init function
    def __init__(self, performance_id: int, zero_hundred: float, break_distance: float, top_speed: float):
        self.__performance_id = performance_id
        self.__zero_hundred = zero_hundred
        self.__break_distance = break_distance
        self.__top_speed = top_speed
    
    # String function
    def __str__(self) -> str:
        return f"Performance n° {self.__performance_id}:\n --0-100 (s): {self.__zero_hundred}\n --Break Distance (m): {self.__break_distance}\n --Top Speed (kph): {self.__top_speed}"

    # Getter and Setter
    @property
    def performance_id(self):
        return self.__performance_id
    @performance_id.setter
    def performance_id(self, value):
        self.__performance_id = value

    @property
    def zero_hundred(self):
        return self.__zero_hundred
    @zero_hundred.setter
    def zero_hundred(self, value):
        self.__zero_hundred = value

    @property
    def break_distance(self):
        return self.__break_distance
    @break_distance.setter
    def break_distance(self, value):
        self.__break_distance = value

    @property
    def top_speed(self):
        return self.__top_speed
    @top_speed.setter
    def top_speed(self, value):
        self.__top_speed = value

@dataclass
class Overview:

    # Init function
    def __init__(self, overview_id: int, manufacturer: str, origin_country: str, introduced_year: int):
        self.__overview_id = overview_id
        self.__manufacturer = manufacturer
        self.__origin_country = origin_country
        self.__introduced_year = introduced_year

    # String function
    def __str__(self) -> str:
        return f"Overview n° {self.__overview_id}:\n --Manufacturer: {self.__manufacturer}\n --Orign Country Drive: {self.__origin_country}\n --Introduced Year: {self.__introduced_year}"

    # Getter and Setter
    @property
    def overview_id(self):
        return self.__overview_id
    @overview_id.setter
    def overview_id(self, value):
        self.__overview_id = value

    @property
    def manufacturer(self):
        return self.__manufacturer
    @manufacturer.setter
    def manufacturer(self, value):
        self.__manufacturer = value

    @property
    def origin_country(self):
        return self.__origin_country
    @origin_country.setter
    def origin_country(self, value):
        self.__origin_country = value

    @property
    def introduced_year(self):
        return self.__introduced_year
    @introduced_year.setter
    def introduced_year(self, value):
        self.__introduced_year = value

#################################

@dataclass
class Vehicle:

    # Init function
    def __init__(self, vehicle_id: int, vehicle_name: str, class_type: str,
                layout: Layout, dimensions: Dimensions, engine: Engine,
                trasmission: Trasmission, performance: Performance, overview: Overview) -> None:
        # local variables
        self.__vehicle_id = vehicle_id
        self.__vehicle_name = vehicle_name
        self.__type = class_type

        # external variables
        self__laps = None
        self.__layout = layout
        self.__dimensions = dimensions
        self.__engine = engine
        self.__trasmission = trasmission
        self.__performance = performance
        self.__overview = overview

    # String function
    def __str__(self) -> str:
        return f"Vehicle n° {self.__vehicle_id}:\n --Name: {self.__vehicle_name}\n --Type: {self.__type}."

    # Getter and Setter
    @property
    def vehicle_id(self):
        return self.__vehicle_id
    @vehicle_id.setter
    def vehicle_id(self, value):
        self.__vehicle_id = value
    
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

    @property
    def laps(self):
        return self.__laps
    @laps.setter
    def laps(self, value):
        self.__laps = value

@dataclass
class Track:
    
    # Init function
    def __init__(self, track_id: int, track_name: str, country: str, total_length: float) -> None:
        # local variables
        self.__track_id = track_id
        self.__track_name = track_name
        self.__country = country
        self.__total_length = total_length

        # external variables
        self.__track_laps = None

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
    def country(self, value):
        self.__country = value
        
    @property
    def total_length(self):
        return self.__total_length
    @total_length.setter
    def total_length(self, value):
        self.__total_length = value
    
    @property
    def track_laps(self):
        return self.__track_laps
    @track_laps.setter
    def track_laps(self, value):
        self.__track_laps = value

@dataclass
class LapTime:

    # Init function
    def __init__(self, lap_id: int, lap_time: float, driver: str, track: Track, vehicle: Vehicle) -> None:
        # local variables
        self.__lap_id = lap_id
        self.__lap_time = lap_time
        self.__driver = driver

        # external variables
        self.__track = track
        self.__vehicle = vehicle

    # String function
    def __str__(self) -> str:
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

#################################

@dataclass
class Car(Vehicle):

    # Init function
    def __init__(self, *args) -> None:
        raise NotImplementedError

@dataclass
class Motorcycle(Vehicle):
    
    # Init function
    def __init__(self, *args) -> None:
        raise NotImplementedError

#################################
