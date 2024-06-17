#!/bin/bash

# Setup environment
if [ ! -d "venv" ]; then
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
fi

# Activate the local Python environment
source venv/bin/activate

# Run all scrapers
python -m src.scrapers.car_and_driver
mv car_and_driver_cars.csv src/data/car_and_driver_cars.csv

python -m src.scrapers.carvana
mv carvana_cars.csv src/data/carvana_cars.csv

python -m src.scrapers.tesla
mv tesla_cars.csv src/data/tesla_cars.csv

python -m src.scrapers.carfax
mv carfax_cars.csv src/data/carfax_cars.csv



