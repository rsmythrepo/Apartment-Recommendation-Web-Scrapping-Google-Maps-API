"""
https://developers.google.com/maps/documentation/places/web-service
"""

from homie import settings
import googlemaps

gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)


class GoogleMaps:
    def get_lat_lng(self, address):
        geocode_result = gmaps.geocode(address)
        lat = geocode_result[0]['geometry']['location']['lat']
        lng = geocode_result[0]['geometry']['location']['lng']
        return lat, lng
        
    def get_category_data(self, category: str):
        places = gmaps.places_nearby(location=(self.lat, self.lng), radius=self.radius, type=category)
        data = []
        for place in places['results']:
            data.append(place['name'])
        return data
    