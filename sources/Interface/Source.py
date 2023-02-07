import requests
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from random_user_agent.user_agent import UserAgent


class Source(ABC):

    @abstractmethod
    def get_specs(user_agent: UserAgent, vehicle: str, url: str, attr: set):
        pass

    @abstractmethod
    def get_layout(specs_map: dict):
        pass
    
    @abstractmethod
    def get_dimensions(specs_map: dict):
        pass

    @abstractmethod
    def get_engine(specs_map: dict):
        pass

    @abstractmethod
    def get_trasmission(specs_map: dict):
        pass

    @abstractmethod
    def get_performance(specs_map: dict):
        pass

    @abstractmethod
    def get_overview(specs_map: dict):
        pass
   