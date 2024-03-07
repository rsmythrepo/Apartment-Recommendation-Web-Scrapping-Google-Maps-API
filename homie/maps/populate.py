from maps.api import GoogleMaps
from sqlmodel import not_, or_, select

from homie.db.models import Flat, Service
from homie.db.session import db_session
from homie.settings import SERVICES

maps_api = GoogleMaps()

@db_session
def populate_services(session):
    # retrive all the addresses from the database
    flats = session.exec(
        select(Flat).where(not_(Flat.services_collected))
    ).all()

    # get the services
    cateogories = SERVICES.split(",")

    for flat in flats:
        for category in cateogories:
            services = maps_api.get_services_by_coordinates(flat, category.name)
            for service in services:
                # todo: define services object
                flat_service = Service(**service)
                session.add(flat_service)

        flat.services_collected = True
        flat.save()
        session.commit()


@db_session
def populate_coordinates(session):
    flats = session.exec(
        select(Flat).where(or_(Flat.latitude is None, Flat.longitude is None))
    ).all()

    for flat in flats:
        lat, lng = maps_api.get_lat_lng(flat.address)
        flat.add_lat_lng(lat, lng)
        session.add(flat)
        session.commit()


def run():
    populate_services()


if __name__ == "__main__":
    run()
