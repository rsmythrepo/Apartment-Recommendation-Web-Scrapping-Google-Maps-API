from maps.api import GoogleMaps
from sqlmodel import select

from homie.db.session import db_session
from homie.db.models import PostalCode

maps_api = GoogleMaps()

@db_session
def populate_services(session):
    # retrive all the addresses from the database
    flats = session.exec(
        select(PostalCode).where(not PostalCode.services_collected)
    ).all()

    flat_postal_codes = list(set([flat.postal_code for flat in flats]))

    for flat in flats:
        for service in services:
            locations = api.get_services_locations(flat, service.name)
            for location in locations:
                # todo: define services object
                flat_service = FlatService(**location)
                session.add(flat_service)

        if flat.lat and flat.lng:
            flat.stage = COORDINATES_COLLECTED
        else:
            flat.stage = SERVICES_COLLECTED
        session.add(flat)
        session.commit()

def run():
    populate_services()


if __name__ == "__main__":
    run()
