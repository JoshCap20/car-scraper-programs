from .base import DynamicScraper
from bs4 import BeautifulSoup
from dataclasses import dataclass

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
    

class TeslaScraper(DynamicScraper):
    teslas: list[Tesla]
    
    def __init__(self):
        super().__init__(url='https://www.tesla.com/inventory/used/m3?arrangeby=plh&zip=28226')
        self.teslas = []
        
    def parse(self):
        self.teslas = []
        
        super().scrape()
        soup = BeautifulSoup(self.data, 'html.parser')
        items = soup.find_all(class_='inventory-content-wrapper')
        
        for item in items:
            result_cards = item.find_all(class_='result card')
            for card in result_cards:
                self.teslas.append(self.parse_card(card))
                
        return self.teslas
        
        
    def parse_card(self, card: str) -> Tesla:
        title = card.find("h3", class_="tds-text--h4").get_text(strip=False)
        year, model = title.split(" ", 1)

        price_text = card.find("span", class_="result-purchase-price tds-text--h4").get_text(strip=True)
        price = float(price_text.replace('$', '').replace(',', ''))

        mileage_div = card.find("div", string=lambda string: string and "mile odometer" in string)
        miles = mileage_div.get_text(strip=True).split(" mile")[0] if mileage_div else "N/A"

        location_div = mileage_div.find_next_sibling("div")
        location = location_div.get_text(strip=False).replace("Available to view in ", "") if location_div else "Unknown"

        payment_div = card.find("div", class_="result-price-monthly-payment")
        estimated_monthly_payment = float(payment_div.get_text(strip=True).split("$")[1].split(" ")[0]) if payment_div else 0.0
 
        # FIX
        transport_fee_div = card.find("div", string=lambda string: string and "Est. Transport Fee" in string)
        estimated_transport_fee_text = transport_fee_div.get_text(strip=False)
        if "No Est. Transport Fee" in estimated_transport_fee_text:
            estimated_transport_fee = 0.0
        else:
            estimated_transport_fee = float(estimated_transport_fee_text.replace("Est. Transport Fee: ", "").replace("$","").replace(",", "")) if transport_fee_div else 0.0

        highlights = card.find("ul", class_="highlights-list")

        range_li = highlights.find("li")
        range = float(range_li.get_text(strip=False).split(" ")[0]) if highlights else 0.0
        
        top_speed_li = range_li.find_next_sibling("li")
        top_speed = float(top_speed_li.get_text(strip=False).split(" ")[0]) if top_speed_li else 0.0
        
        acceleration_li = top_speed_li.find_next_sibling("li")
        acceleration = float(acceleration_li.get_text(strip=False).split(" ")[0]) if acceleration_li else 0.0

        color_li = card.find("li", string=lambda string: string and "Paint" in string)
        color = color_li.get_text(strip=True) if color_li else "Unknown"

        interior_li = card.find("li", string=lambda string: string and "Interior" in string)
        interior = interior_li.get_text(strip=True) if interior_li else "Unknown"

        wheels_li = card.find("li", string=lambda string: string and "Wheels" in string)
        wheels = wheels_li.get_text(strip=True) if wheels_li else "Unknown"

        full_self_driving_li = card.find("span", class_="inventory-icon--autopilot-fsd")
        full_self_driving = full_self_driving_li is not None

        reported_accidents_li = card.find("span", class_="inventory-icon--history-repair")
        reported_accidents = reported_accidents_li is not None

        return Tesla(
            year=year,
            model=model,
            price=price,
            miles=miles,
            location=location,
            estimated_monthly_payment=estimated_monthly_payment,
            estimated_transport_fee=estimated_transport_fee,
            range=range,
            top_speed=top_speed,
            acceleration=acceleration,
            color=color,
            interior=interior,
            wheels=wheels,
            full_self_driving=full_self_driving,
            reported_accidents=reported_accidents
        )
            
if __name__ == '__main__':
    scraper = TeslaScraper()
    scraper.parse()
    print(scraper.teslas)
    print(f"Found {len(scraper.teslas)} Teslas!")
    # check for repeats
    repeats = 0
    for i, tesla in enumerate(scraper.teslas):
        for j in range(i+1, len(scraper.teslas)):
            if tesla.price == scraper.teslas[j].price and tesla.miles == scraper.teslas[j].miles:
                repeats += 1
    print(f"Found {repeats} repeated Teslas!")