import time
import schedule

from ..scrapers import TeslaScraper
from ..comm import (
    AzureEmailCommunicationClient as EmailClient,
    AzureSMSCommunicationClient as SMSClient,
)


def find_best_deal(mileage_threshold: int):
    scraper = TeslaScraper()
    data = scraper.parse()

    best_deals = [
        tesla
        for tesla in data
        if int(tesla.miles.replace(",", "")) <= mileage_threshold
    ]
    best_deals.sort(key=lambda x: x.price + x.estimated_transport_fee)

    if best_deals:
        best_deal = best_deals[0]
        message = f"Results in total: {len(data)}\nResults within mileage threshold: {len(best_deals)}\n"
        message += (
            f"Best Deal Found:\n"
            f"{best_deal.year} {best_deal.model}\n"
            f"Price: ${best_deal.price}\tEst. Monthly Payment: ${best_deal.estimated_monthly_payment}\n"
            f"Miles: {best_deal.miles}\n"
            f"Location: {best_deal.location}\tEst. Transport Fee: ${best_deal.estimated_transport_fee}\n"
            f"Range: {best_deal.range} miles\tTop Speed: {best_deal.top_speed} mph\tAcceleration: {best_deal.acceleration} s\n"
            f"Color: {best_deal.color}\tInterior: {best_deal.interior}\tWheels: {best_deal.wheels}\n"
            f"Full Self-Driving: {'Yes' if best_deal.full_self_driving else 'No'}\tReported Accidents: {'Yes' if best_deal.reported_accidents else 'No'}\n"
        )

        print(message)

        if len(best_deals) > 1:
            message += "\nOther Options:\n"
            i = 0
            for deal in best_deals[1:]:
                message += (
                    f"{deal.year} {deal.model}"
                    f"\nPrice: ${deal.price}\tEst. Monthly Payment: ${deal.estimated_monthly_payment}"
                    f"\nMiles: {deal.miles}"
                    f"\nLocation: {deal.location}\tEst. Transport Fee: ${deal.estimated_transport_fee}"
                    f"\nColor: {deal.color}\tInterior: {deal.interior}\tWheels: {deal.wheels} "
                    f"\nFull Self-Driving: {'Yes' if deal.full_self_driving else 'No'}\tReported Accidents: {'Yes' if deal.reported_accidents else 'No'} \n\n"
                )
                i += 1
                if i > 10:
                    break

        subject = (
            f"Tesla Alert for ${best_deal.price} {best_deal.year} {best_deal.miles}mi"
        )
        EmailClient.send_email(message=message, subject=subject)

        if best_deal.price + best_deal.estimated_transport_fee <= 25000:
            SMSClient.send_sms(msg="[REBATE ELGIBILE] " + subject)
        elif best_deal.price <= 25000:
            SMSClient.send_sms(msg="[SUB 25K] " + subject)

    else:
        print("No deals found within the mileage threshold.")


def job():
    """
    Job to run every 20 minutes.
    """
    mileage_threshold = 50000  # Set your mileage threshold
    print(
        f"[{time.time}] Searching for deals with mileage threshold of {mileage_threshold}..."
    )
    find_best_deal(mileage_threshold)


# Schedule the job every 20 minutes
job()
schedule.every(20).minutes.do(job)

print("Starting Tesla Deal Finder CLI...")

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
