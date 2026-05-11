import uuid
import random
import time
import sys
import os
from datetime import datetime, timedelta

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from services.blockchain_service import blockchain_service

PRODUCT_NAMES = ["Organic Carrots", "King Coconuts", "Red Onions", "Keells Bananas", "Hill Country Tomatoes", "Gotu Kola"]
FARM_LOCATIONS = ["Green Acres Farm, Nuwara Eliya", "Sun-Kissed Grove, Dambulla", "Royal Gardens, Kandy", "Coastal Fields, Matara"]
DIST_CENTERS = ["Central Distribution Hub, Colombo", "Regional Warehouse, Gampaha"]
RETAIL_STORES = ["FreshMart, Colombo 07", "SuperGrocer, Galle", "City Foods, Kandy"]

FARMER_USER = "farmer1@example.com"
DISTRIBUTOR_USER = "dist1@example.com"
RETAILER_USER = "retail1@example.com"

def generate_simulated_data(num_products=25):
    print(f"--- Starting data simulation for {num_products} products. ---")

    for i in range(num_products):
        product_id = str(uuid.uuid4())
        product_name = random.choice(PRODUCT_NAMES)
        farm_location = random.choice(FARM_LOCATIONS)
        harvest_time = datetime.now() - timedelta(days=random.randint(5, 10)) # Start journey further in the past
        print(f"\n({i+1}/{num_products}) Simulating journey for: {product_name} (ID: {product_id[:8]}...)")

        # --- a. Farmer Registers the Product ---
        tx_data_farmer = {
            "product_id": product_id, "product_name": product_name, "sender": FARMER_USER,
            "recipient": DISTRIBUTOR_USER, "location": farm_location,
            "temperature": round(random.uniform(22.0, 26.0), 1),
            "humidity": round(random.uniform(75.0, 85.0), 1),
            "transport_info": "Harvested and packed in crates.", "status": "Registered",
            "timestamp": harvest_time.timestamp()
        }
        blockchain_service.add_transaction(tx_data_farmer)
        print(f" -> Farmer registered product at {farm_location}")
        time.sleep(0.5) 

        # --- b. Distributor Receives and Ships the Product ---
        # Make the journey from farm to distributor take 1-3 days
        dist_arrival_time = harvest_time + timedelta(days=random.randint(1, 3), hours=random.randint(0, 12))
        dist_location = random.choice(DIST_CENTERS)
        
        is_anomaly = (i % 4 == 0)
        temp_at_distributor = round(random.uniform(30.0, 35.0), 1) if is_anomaly else round(random.uniform(12.0, 16.0), 1)
        
        tx_data_distributor = {
            "product_id": product_id, "product_name": product_name, "sender": DISTRIBUTOR_USER,
            "recipient": RETAILER_USER, "location": dist_location,
            "temperature": temp_at_distributor, "humidity": round(random.uniform(80.0, 90.0), 1),
            "transport_info": "Stored in refrigerated unit. ANOMALY DETECTED." if is_anomaly else "Stored in refrigerated unit.",
            "status": "In Transit", "timestamp": dist_arrival_time.timestamp()
        }
        blockchain_service.add_transaction(tx_data_distributor)
        print(f" -> Distributor processed at {dist_location}. {'**ANOMALY: High Temp**' if is_anomaly else ''}")
        time.sleep(0.5)

        # --- c. Retailer Stocks the Product ---
        # Make the journey from distributor to retailer take 6-18 hours
        retail_arrival_time = dist_arrival_time + timedelta(hours=random.randint(6, 18))
        retail_location = random.choice(RETAIL_STORES)
        
        tx_data_retailer = {
            "product_id": product_id, "product_name": product_name, "sender": RETAILER_USER,
            "recipient": "consumer", "location": retail_location,
            "temperature": round(random.uniform(18.0, 22.0), 1),
            "humidity": round(random.uniform(60.0, 70.0), 1),
            "transport_info": "Received and displayed in store.", "status": "In Stock",
            "timestamp": retail_arrival_time.timestamp()
        }
        blockchain_service.add_transaction(tx_data_retailer)
        print(f" -> Retailer stocked at {retail_location}")

    print("\n--- Simulation complete. Blockchain has been populated. ---")

if __name__ == "__main__":
    generate_simulated_data(num_products=25)