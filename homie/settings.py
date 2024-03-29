import os

from dotenv import load_dotenv

load_dotenv()

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
GOOGLE_MAPS_DEFAULT_RADIUS = int(os.getenv("GOOGLE_MAPS_DEFAULT_RADIUS", 1000))
SERVICES = os.getenv("SERVICES", "supermarket,subway_station,bus_station")
