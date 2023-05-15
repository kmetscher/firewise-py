from enum import Enum
from datetime import datetime, time

import numpy

class Category(Enum):
    NATURAL = 0
    HUMAN = 1
    
class Cause(Enum):
    ARSON = 0 
    BURNING_DEBRIS = 1
    EQUIPMENT_USE = 2
    FIREARMS_EXPLOSIVES = 3
    FIREWORKS = 4
    MISUSE_BY_MINOR = 5
    NATURAL = 6
    POWER_INFRASTRUCTURE = 7
    RAILROAD = 8
    RECREATION_CEREMONY = 9
    SMOKING = 10
    OTHER = 11
    UNKNOWN = 12

class Fire:

    def _canonicalize_cause(self, string: str) -> Cause:
        if "power" in string:
            return Cause.POWER_INFRASTRUCTURE
        if "debris" in string:
            return Cause.BURNING_DEBRIS
        if "equipment" in string:
            return Cause.EQUIPMENT_USE
        if "Firearms" in string:
            return Cause.FIREARMS_EXPLOSIVES
        if "minor" in string:
            return Cause.MISUSE_BY_MINOR
        if "Natural" in string:
            return Cause.NATURAL
        if "Arson" in string:
            return Cause.ARSON
        if "Railroad" in string:
            return Cause.RAILROAD
        if "Recreation" in string:
            return Cause.RECREATION_CEREMONY
        if "Smoking" in string:
            return Cause.SMOKING
        if "Unknown" in string:
            return Cause.UNKNOWN
        return Cause.OTHER

    def __init__(self, fpa_id: str, name: str, cause: str, 
            discovery_date: datetime, discovery_time: time, 
            discovery_doy: int, containment_date: datetime, 
            containment_time: time, containment_doy: int,
            size: float, latitude: float, longitude: float, 
            state: str) -> None:
        self.fpa_id = fpa_id
        self.name = name
        self.cause = self._canonicalize_cause(cause)
        if self.cause is not Cause.NATURAL:
            self.category = Category.HUMAN
        else: 
            self.category = Category.NATURAL
        self.discovery_date = discovery_date
        self.discovery_time = discovery_time
        self.discovery_doy = discovery_doy
        self.containment_date = containment_date
        self.containment_time = containment_time
        self.containment_doy = containment_doy
        self.size = size
        self.latitude = latitude
        self.longitude = longitude
        self.state = state
        
    def get_independent_attributes(self, np = False) -> list | numpy.ndarray:
        attributes = [int(self.discovery_date.timestamp()), 
                self.discovery_time,
                self.discovery_doy,
                int(self.containment_date.timestamp()), 
                self.containment_time,
                self.containment_doy,
                float(self.latitude), 
                float(self.longitude),
                self.size]
        if np:
            return numpy.array(attributes)
        return attributes

    def pretty_print(self) -> None:
        print("{}: {}, {}".format(self.fpa_id, self.name, self.state))
        print("    {} to {}, {} acre(s) burned".format(self.discovery_date, self.containment_date, self.size))
        print("    {}: {}".format(self.cause.value, self.cause.name))
