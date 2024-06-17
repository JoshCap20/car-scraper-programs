from dataclasses import dataclass
from enum import Enum

class Source(Enum):
    CARMAX = 'carmax'
    TESLA = 'tesla'
    CAR_AND_DRIVER = 'car_and_driver'
    CARFAX = 'carfax'
    CARVANA = 'carvana'
    
    
@dataclass
class Tesla:
    year: str
    model: str
    price: float
    miles: str
    location: str
    estimated_monthly_payment: float
    estimated_transport_fee: float
    range: float
    top_speed: float
    acceleration: float
    color: str
    interior: str
    wheels: str
    full_self_driving: bool
    reported_accidents: bool
    
    
@dataclass
class Car:
    year: int
    make: str
    model: str
    price: int
    miles: int
    # location: str
    # color: str
    # wheels: str
    rating: str
    source: Source
    