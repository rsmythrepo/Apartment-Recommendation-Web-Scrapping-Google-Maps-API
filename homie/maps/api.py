"""
https://developers.google.com/maps/documentation/places/web-service
"""

import googlemaps

from homie import settings
from homie.db.models import FlatService

gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)


class GoogleMaps:
    def get_lat_lng(self, address):
        """
        expected payload format:
        type: list
        payload: [
            {
                'address_components': [
                    {
                        'long_name': '1600',
                        'short_name': '1600',
                        'types': ['street_number']
                    },
                    {
                        'long_name': 'Amphitheatre Parkway',
                        'short_name': 'Amphitheatre Pkwy',
                        'types': ['route']
                    },
                    {
                        'long_name': 'Mountain View',
                        'short_name': 'Mountain View',
                        'types': ['locality', 'political']
                    },
                    {
                        'long_name': 'Santa Clara County',
                        'short_name': 'Santa Clara County',
                        'types': ['administrative_area_level_2', 'political']
                    },
                    {
                        'long_name': 'California',
                        'short_name': 'CA',
                        'types': ['administrative_area_level_1', 'political']
                    },
                    {
                        'long_name': 'United States',
                        'short_name': 'US',
                        'types': ['country', 'political']
                    },
                    {
                        'long_name': '94043',
                        'short_name': '94043',
                        'types': ['postal_code']
                    }
                ],
                'formatted_address': '1600 Amphitheatre Pkwy, Mountain View, CA 94043, USA',
                'geometry': {
                    'location': {
                        'lat': 37.4215983,
                        'lng': -122.083622
                    },
                    'location_type': 'ROOFTOP',
                    'viewport': {
                        'northeast': {'lat': 37.4227428302915, 'lng': -122.0823176697085},
                        'southwest': {'lat': 37.42004486970851, 'lng': -122.0850156302915}
                    }
                },
                'place_id': 'ChIJUweKxpq7j4AR5Hhj5b3ikS4',
                'plus_code': {
                    'compound_code': 'CWC8+JH Mountain View, CA',
                    'global_code': '849VCWC8+JH'
                }, 'types': ['street_address']
            }
        ]
        """
        geocode_result = gmaps.geocode(address)
        lat = geocode_result[0]['geometry']['location']['lat']
        lng = geocode_result[0]['geometry']['location']['lng']
        return lat, lng

    def get_services_around(self, lat: float, lng: float, service: str) -> list[FlatService]:
        """
        source: https://developers.google.com/maps/documentation/places/web-service/search-nearby
        expected payload format:
        type: dict
        payload: {
            'html_attributions': [],
            'next_page_token': '...',
            'results': [
                {
                    'business_status': 'OPERATIONAL',
                    'geometry': {
                        'location': {'lat': 37.407464, 'lng': -122.1203004},
                        'viewport': {
                            'northeast': {'lat': 37.4086840302915, 'lng': -122.1190276697085},
                            'southwest': {'lat': 37.4059860697085, 'lng': -122.1217256302915}
                        }
                    },
                    'icon': 'https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/lodging-71.png',
                    'icon_background_color': '#909CE1',
                    'icon_mask_base_uri': 'https://maps.gstatic.com/mapfiles/place_api/icons/v2/hotel_pinlet',
                    'name': "Dinah's Garden Hotel",
                    'photos': [
                        {
                            'height': 1195,
                            'html_attributions': [
                                '<a
                                    href="https://maps.google.com/maps/contrib/115212688446356792868"
                                >Dinah&#39;s Garden Hotel</a>'
                            ],
                            'photo_reference': '...',
                            'width': 1800
                        }
                    ],
                    'place_id': 'ChIJxUf2lnm6j4ARf-dI1c4L9sA',
                    'plus_code': {
                        'compound_code': 'CV4H+XV Palo Alto, CA, USA',
                        'global_code': '849VCV4H+XV'
                    },
                    'rating': 4.5,
                    'reference': 'ChIJxUf2lnm6j4ARf-dI1c4L9sA',
                    'scope': 'GOOGLE',
                    'types': [
                        'lodging', 'restaurant', 'food', 'point_of_interest', 'establishment'
                    ],
                    'user_ratings_total': 1025,
                    'vicinity': '4261 El Camino Real, Palo Alto'
                }
            ],
            'status': 'OK'
        }
        """
        services = []
        next_page_token = None

        while True:
            payload = gmaps.places_nearby(
                location=(lat, lng),
                type=service,
                radius=settings.GOOGLE_MAPS_DEFAULT_RADIUS,
                pagetoken=next_page_token
            )

            next_page_token = payload.get('next_page_token')
            for place in payload['results']:
                flat_service = FlatService(
                    latitude=lat,
                    longitude=lng,
                    name=place['name'],
                    business_status=place['business_status'],
                    rating=place['rating'],
                    types=",".join(place['types']),
                    user_ratings_total=place['user_ratings_total'],
                    vicinity=place['vicinity'],
                    original_type=service
                )
                services.append(flat_service)

            if not next_page_token:
                break

        return services


if __name__ == "__main__":
    maps = GoogleMaps()
    # 'lat': 37.4215983, 'lng': -122.083622
    geocode_result = maps.get_services_around(37.4215983, -122.083622, "restaurant")
