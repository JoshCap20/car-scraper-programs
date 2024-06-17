from .base import Scraper
from .models import Car, Source
import requests
import csv

class CarfaxScraper(Scraper):
    URL: str = "https://helix.carfax.com/search/v2/vehicles?zip=28263&radius=100&sort=BEST&vehicleCondition=USED&tpType=RBS&tpPositions=1%2C2%2C3&dynamicRadius=false&fetchImageLimit=6&tpQualityThreshold=150&tpValueBadges=GOOD%2CGREAT&urlInfo=Used-Cars-Under-50000_f11"
    
    def __init__(self, page: int = 1, max_pages: int = 0):
        super().__init__(url=self.URL)
        self.cars = []
        self.max_pages = max_pages
        self.page = page
        
    def scrape(self):
        data = self.api_request()
        
        if self.max_pages == 0:
            self.max_pages = data["totalPageCount"]
            print(f"Max pages set to: {self.max_pages}")

        self.parse_cars(data)
        
        for i in range(2, self.max_pages + 1):
            self.page = i
            data = self.api_request(page=self.page)
            self.parse_cars(data)
            
        self.output_to_csv(self.cars)
    
    def api_request(self, page: int = 1, min_year: int = 2020, max_price: int = 50000):
        return requests.get(self.URL + f"&page={page}&priceMax={max_price}&yearMin={min_year}").json()
    
    def parse_cars(self, data):
        [self.cars.append(self.parse_car(car)) for car in data["listings"]]
        
    def parse_car(self, car):
        return Car(
            year=car["year"],
            make=car["make"],
            model=car["model"],
            price=car["currentPrice"],
            miles=car["mileage"],
            rating="N/A",
            source=Source.CARFAX
        )
        
    @staticmethod
    def output_to_csv(cars):
        # export to csv
        with open('carfax_cars.csv', mode='w') as file:
            writer = csv.writer(file)
            writer.writerow(["Year", "Make", "Model", "Price", "Miles", "Rating", "Source"])
            for car in cars:
                writer.writerow([car.year, car.make, car.model, car.price, car.miles, car.rating, car.source])
                
if __name__ == '__main__':
    scraper = CarfaxScraper()
    scraper.scrape()
        
        