from abc import ABC, abstractmethod

class Source(ABC):

    @abstractmethod
    def get_specs(url: str, attr: set):
        # Method for get all specs in a specific website ad-hoc
        # :param url: the target site url.
        # :param attr: a set of specific attributes (see database structure).
        # :return: should return a specific dictionary that contains all key-values.
        pass

    @abstractmethod
    def get_layout(self, specs_map: dict):
        # Method for get all specific layout attributes
        # :param specs_map: a dict with all specs mapped for specific value in the website.
        # :return: should return a dict of key-values compliant to database.
        pass
    
    @abstractmethod
    def get_dimensions(self, specs_map: dict):
        # Method for get all specific dimensions attributes
        # :param specs_map: a dict with all specs mapped for specific value in the website.
        # :return: should return a dict of key-values compliant to database.
        pass

    @abstractmethod
    def get_engine(self, specs_map: dict):
        # Method for get all specific engine attributes
        # :param specs_map: a dict with all specs mapped for specific value in the website.
        # :return: should return a dict of key-values compliant to database.
        pass

    @abstractmethod
    def get_trasmission(self, specs_map: dict):
        # Method for get all specific trasmisison attributes
        # :param specs_map: a dict with all specs mapped for specific value in the website.
        # :return: should return a dict of key-values compliant to database.
        pass

    @abstractmethod
    def get_performance(self, specs_map: dict):
        # Method for get all specific performance attributes
        # :param specs_map: a dict with all specs mapped for specific value in the website.
        # :return: should return a dict of key-values compliant to database.
        pass
