import csv
import logging
import os

from db.models import Flat
from db.session import db_session

logger = logging.getLogger("homie")


class CSVUploader:
    def read_file(self, file_path: str):
        if not os.path.exists(file_path):
            logger.error(f"File does not exist: {file_path}")
            raise ValueError(f"File does not exist: {file_path}")

        with open(file_path) as file:
            reader = csv.DictReader(file)
            data = [row for row in reader]
            return data

    @db_session
    def populate(self, file_path: str, session=None):
        flats_data = self.read_file(file_path)

        for data in flats_data:
            flat = Flat(**data)
            session.add(flat)
        session.commit()

        logger.info(f"{len(flats_data)} flats added")

