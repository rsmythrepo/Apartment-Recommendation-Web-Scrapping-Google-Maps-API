from maps.api import GoogleMaps
from sqlmodel import select

from homie.db.models import PostalCode
from homie.db.session import db_session
from homie.settings import SERVICES

maps_api = GoogleMaps()

@db_session
def populate_services(session):
    # retrive all the addresses from the database
    postal_codes = session.exec(
        select(PostalCode).where(PostalCode.services_collected != True).distinct(PostalCode.code)  # noqa
    ).all()

    service_terms = SERVICES.split(",")

    for postal_code in postal_codes:
        for term in service_terms:
            services = maps_api.get_services_by_postal_code(term, postal_code)
            session.bulk_save_objects(services)

        postal_code.services_collected = True
        session.add(postal_code)
        session.commit()

def run():
    populate_services()


if __name__ == "__main__":
    run()
