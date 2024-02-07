from db.models import Flat, FlatService, ServiceCategory
from googlemaps.api import GoogleMaps
from sqlmodel import or_, select

from homie.db.session import db_session

api = GoogleMaps()

@db_session
def populate_services(session):
    # retrive all the addresses from the database
    flats = session.exec(
        select(Flat).where(Flat.services_collected)
    ).all()

    # get the services
    cateogories = session.query(ServiceCategory).all()

    for flat in flats:
        for category in cateogories:
            services = api.get_flat_services(flat, category.name)
            for service in services:
                # todo: define services object
                flat_service = FlatService(**service)
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
        lat, lng = api.get_lat_lng(flat.address)
        flat.add_lat_lng(lat, lng)
        session.add(flat)
        session.commit()
