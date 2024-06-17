import re
from .base import Scraper
from .models import Car, Source
import csv


class CarAndDriverScraper(Scraper):
    cars: list[Car]
    URL = "https://shopping.caranddriver.com/used-cars-for-sale/listings/year-2020-2024/price-below-30000/location-charlotte-nc/?mileageHigh=100000&searchRadius=100"
    
    def __init__(self, page: int = 1, max_pages: int = 0):
        super().__init__(url=self.URL)
        self.page = page
        self.max_pages = max_pages
        self.cars = []
        
    def run(self):
        super().scrape()
        if self.max_pages == 0:
            self.parse_max_pages()
        self.parse_listings()
            
        for i in range(2, self.max_pages + 1):
            self.page = i
            self.url = self.URL + f"&page={self.page}"
            self.scrape()
            self.parse_listings()
        self.output_to_csv(self.cars)
        
    def parse_max_pages(self):
        pagination_items = self.data.find_all("li", {"data-test": "paginationItem"})
        if pagination_items:
            self.max_pages = int(pagination_items[-1].text.strip())
            print(f"Max pages set to: {self.max_pages}")
    
    def parse_listings(self):
        data = self.data.find("div", {"data-test": "allVehicleListings"})
        listings = data.find_all("li", {"class": "mt-3 flex grow col-md-6 col-xl-4"})
        [self.parse_listing(listing) for listing in listings]
        
    def parse_listing(self, listing):
        try:
            vehicleCardInfo = listing.find("div", {"data-test": "vehicleCardInfo"})
            vehicleConditionYearMake = vehicleCardInfo.find("div", {"data-test": "vehicleCardConditionYearMake"})
            make = vehicleConditionYearMake.text.split(" ")[-1]
            model_trim = vehicleCardInfo.find("div", {"data-test": "vehicleCardTrim"}).text
            price = listing.find("span", {"data-test": "vehicleCardPriceLabelAmount"}).text
            try:
                rating = listing.find("span", {"data-test": "graphIconLabel"}).text
            except AttributeError:
                rating = "N/A"
            miles = listing.find("div", {"data-test": "vehicleMileage"}).text
            
            car = Car(
                year=int(self.extract_year(vehicleConditionYearMake.text)),
                make=make,
                model=model_trim,
                price=int(price.replace("$", "").replace(",", "")),
                miles=int(miles.replace("mi", "").replace(",", "").replace("k", "000")),
                # location="Charlotte, NC",
                rating=rating,
                # color="",
                # wheels="",
                source=Source.CAR_AND_DRIVER
            )
            print(car)
            self.cars.append(car)
        except Exception as e:
            print(f"Error parsing listing: {e}")
        
    @staticmethod
    def output_to_csv(cars):
        # export to csv
        with open('car_and_driver_cars.csv', mode='w') as file:
            writer = csv.writer(file)
            writer.writerow(["Year", "Make", "Model", "Price", "Miles", "Rating", "Source"])
            for car in cars:
                writer.writerow([car.year, car.make, car.model, car.price, car.miles, car.rating, car.source])
        
    @staticmethod
    def extract_year(vehicle_condition_year_make: str):
        match = re.search(r"\b(19|20)\d{2}\b", vehicle_condition_year_make)
        if match:
            year = int(match.group(0))
            return year
        return None
    
if __name__ == "__main__":
    scraper = CarAndDriverScraper(max_pages=0)
    scraper.run()
    print(scraper.cleaned_data)
    print(scraper.cars)