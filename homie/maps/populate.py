from db.models import Flat, FlatService
from maps.api import GoogleMaps
from sqlmodel import select

from homie.db.session import db_session

api = GoogleMaps()

@db_session
def populate_services(session):
    # retrive all the addresses from the database
    flats = session.exec(
        select(Flat).where(stage=DATA_COLLECTED)
    ).all()

    # get the services
    services = session.query(FlatService).all()

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
