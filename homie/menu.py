import logging

from db.engine import create_db_and_tables
import os
from files.populate import run as files_populate

"""
from maps.populate import run as googlemaps_populate
from scrappers.populate import run as scrappers_populate

"""

logger = logging.getLogger("homie")


if __name__ == "__main__":
    print("SELECT AN OPTION")
    print("1. Populate database from CSV")
    print("2. Populate database from scrappers")
    print("3. Search for services using Google Maps API")

    option = input("Option: ")

    logger.info("Creating database and tables")
    create_db_and_tables()

    match option:
        case "1":
            file_path = "files/templates/flats.csv"  # input("Enter the file path: ")
            base_path = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(base_path, file_path)
            files_populate(file_path)
        case "2":
            # todo @raph
            # scrappers_populate()
            pass
        case "3":
            # WIP
            # googlemaps_populate()
            pass
        case _:
            logger.error("Invalid option")
