from .models import Car, Source
import requests
import csv

class CarvanaScraper:
    cars: list[Car]
    API_URL = "https://apik.carvana.io/merch/search/api/v2/search"
    
    def __init__(self, page: int = 1, max_pages: int = 0):
        self.cars = []
        self.max_pages = max_pages
        self.page = page
        
    def scrape(self):
        data = self.api_request()
        self.parse_cars(data)
        self.get_total_pages(data)
        
        for i in range(2, self.max_pages + 1):
            self.page = i
            data = self.api_request(page=self.page)
            self.parse_cars(data)
            
        print(self.cars)
        self.output_to_csv(self.cars)
    
    def get_total_pages(self, data):
        self.max_pages = data['inventory']['pagination']['totalMatchedPages']
    
    def api_request(self, page: int = 1, pageSize: int = 100, zipCode: str = "28226"):
        url = "https://apik.carvana.io/merch/search/api/v2/search"
        url += f"?page={page}"
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.8",
            "authorization": "Bearer",
            "content-type": "application/json",
            "priority": "u=1, i",
            "sec-ch-ua": "\"Chromium\";v=\"124\", \"Brave\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"macOS\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "cross-site",
            "sec-gpc": "1"
        }
        body = {
            "analyticsData": {
                "browser": "Chrome",
                "clientId": "srp_ui",
                "deviceName": "",
                "isFirstActiveSearchSession": False,
                "isMobileDevice": False,
                "previousSearchRequestId": "6e763a96-57bb-4814-9c5e-00071fac46a7",
                "referrer": "",
                "searchSessionId": "19da31e1-d859-4be9-9ae4-363536ea50a9"
            },
            "browserCookieId": "69f1d404-5a19-d630-f059-f1253249efa8",
            "filters": {},
            "pagination": {
                "page": page,
                "pageSize": pageSize
            },
            "requestedFeatures": [
                "EarliestAcquisitionBoosting",
                "ExcludeFacetData",
                "LoanTermPricing",
                "LocationBasedPrefiltering",
                "Personalization",
                "Sprinkles",
                "HideImpossibleCombos",
                "ApplyTradeIn"
            ],
            "sortBy": "MostPopular",
            "zip5": zipCode
        }

        response = requests.post(url, headers=headers, json=body)
        
        return response.json()
        
    def parse_cars(self, data):
        for vehicle in data['inventory']['vehicles']:
            car = Car(
                year=vehicle['year'],
                make=vehicle['make'],
                model=vehicle['model'],
                price=vehicle['price']['total'],
                miles=vehicle['mileage'],
                rating=vehicle.get('kbbTrim', 'N/A'),  # Using 'kbbTrim' as a proxy for rating
                source=Source.CARVANA,
            )
            print(car)
            self.cars.append(car)
            
    @staticmethod
    def output_to_csv(cars):
        # export to csv
        with open('carvana_cars.csv', mode='w') as file:
            writer = csv.writer(file)
            writer.writerow(["Year", "Make", "Model", "Price", "Miles", "Rating"])
            for car in cars:
                writer.writerow([car.year, car.make, car.model, car.price, car.miles, car.rating])
        
        
if __name__ == "__main__":
    scraper = CarvanaScraper()
    scraper.scrape()