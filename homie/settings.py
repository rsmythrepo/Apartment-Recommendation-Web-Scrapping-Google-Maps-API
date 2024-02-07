from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
GOOGLE_MAPS_DEFAULT_RADIUS = int(os.getenv("GOOGLE_MAPS_DEFAULT_RADIUS", 5000))