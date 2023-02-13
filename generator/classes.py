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
        return f"Layout n° {self.__layout_id}:\n --Layout: {self.__engine_layout}\n --Wheel Drive: {self.__wheel_drive}\n --Class Type: {self.__class_type}"

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
    def __init__(self, dim_id: int, curb_weight: float, wheelbase: float, length: float, width: float, height: float):
        self.__dim_id = dim_id
        self.__curb_weight = curb_weight
        self.__wheelbase = wheelbase
        self.__length = length
        self.__width = width
        self.__height = height
    
    # String function
    def __str__(self) -> str:
        return f"Dimensions n° {self.__dim_id}:\n --Curb Weight: {self.__curb_weight}\n --Wheelbase: {self.__wheelbase}\n --Length: {self.__length}\n  --Wide: {self.__width}\n --Heigth: {self.__height}"

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
    def length(self):
        return self.__length
    @length.setter
    def length(self, value):
        self.__length = value

    @property
    def width(self):
        return self.__width
    @width.setter
    def width(self, value):
        self.__width = value

    @property
    def height(self):
        return self.__height
    @height.setter
    def height(self, value):
        self.__height = value
@dataclass
class Engine:

    # Init function
    def __init__(self, engine_id: int, engine_name: str, displacement: float, power: int, torque: int):
        self.__engine_id = engine_id
        self.__engine_name = engine_name
        self.__displacement = displacement
        self.__power = power
        self.__torque = torque

    # String function
    def __str__(self) -> str:
        return f"Engine n° {self.__engine_id}:\n --Engine: {self.__engine_name}\n --Displacement: {self.__displacement}\n --Power: {self.__power}\n --Torque: {self.__torque}"

    # Getter and Setter
    @property
    def engine_id(self):
        return self.__engine_id
    @engine_id.setter
    def engine_id(self, value):
        self.__engine_id = value
    
    @property
    def engine_name(self):
        return self.__engine_name
    @engine_name.setter
    def engine_name(self, value):
        self.__engine_name = value
    
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
    def __init__(self, performance_id: int, accelleration: float, break_distance: float, top_speed: float):
        self.__performance_id = performance_id
        self.__accelleration = accelleration
        self.__break_distance = break_distance
        self.__top_speed = top_speed
    
    # String function
    def __str__(self) -> str:
        return f"Performance n° {self.__performance_id}:\n --0-100 (s): {self.__accelleration}\n --Break Distance (m): {self.__break_distance}\n --Top Speed (kph): {self.__top_speed}"

    # Getter and Setter
    @property
    def performance_id(self):
        return self.__performance_id
    @performance_id.setter
    def performance_id(self, value):
        self.__performance_id = value

    @property
    def accelleration(self):
        return self.__accelleration
    @accelleration.setter
    def accelleration(self, value):
        self.__accelleration = value

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

#################################

@dataclass
class Vehicle:

    # Init function
    def __init__(self, vehicle_id: int, vehicle_name: str, vehicle_type: str, manufacturer: str, model: str, origin_country: str, introduced_year: str,
                layout: Layout, dimensions: Dimensions, engine: Engine,
                trasmission: Trasmission, performance: Performance) -> None:
        # local variables
        self.__vehicle_id = vehicle_id
        self.__vehicle_name = vehicle_name
        self.__vehicle_type = vehicle_type
        self.__manufacturer = manufacturer
        self.__model = model
        self.__origin_country = origin_country
        self.__introduced_year = introduced_year

        # external variables
        self__laps = None
        self.__layout = layout
        self.__dimensions = dimensions
        self.__engine = engine
        self.__trasmission = trasmission
        self.__performance = performance

    # String function
    def __str__(self) -> str:
        return f"Vehicle n° {self.__vehicle_id}:\n --Name: {self.__vehicle_name}\n --Type: {self.__vehicle_type}\n --Manufacturer: {self.__manufacturer}\n --Model: {self.__model}."

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
    def vehicle_type(self):
        return self.__vehicle_type
    @vehicle_type.setter
    def vehicle_type(self, value):
        self.__vehicle_type = value
    
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
    def laps(self):
        return self.__laps
    @laps.setter
    def laps(self, value):
        self.__laps = value

    @property
    def manufacturer(self):
        return self.__manufacturer
    @manufacturer.setter
    def manufacturer(self, value):
        self.__manufacturer = value

    @property
    def model(self):
        return self.__model
    @model.setter
    def model(self, value):
        self.__model = value

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
