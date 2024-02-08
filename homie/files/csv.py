import csv
import logging
import os
from datetime import datetime

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
            data = self.format_data(data)
            flat = Flat(**data)
            session.add(flat)
        session.commit()

        logger.info(f"{len(flats_data)} flats added")

    def format_data(self, data):
        datetime_fields = ["published_at", "updated_at"]
        for field in datetime_fields:
            value = data.get(field)
            if value:
                data[field] = datetime.strptime(value, "%Y-%m-%d")
            else:
                data[field] = None
        
        bool_fields = [
            "has_balcony", "has_heating", "allow_pets", "allow_kids",
            "exterior", "has_elevator", "has_air_conditioning",
            "has_energy_certification"
        ]
        for field in bool_fields:
            value = data.get(field)
            if value:
                data[field] = value.lower() == "true"
            else:
                data[field] = None
        
        float_fields = [
            "price", "price_per_m2", "energy_consumption", "energy_emissions"
        ]
        for field in float_fields:
            value = data.get(field)
            if value:
                data[field] = float(value)
            else:
                data[field] = None
        
        int_fields = ["space", "rooms", "bathrooms", "built_on", "max_guests"]
        for field in int_fields:
            value = data.get(field)
            if value:
                data[field] = int(value)
            else:
                data[field] = None
        
        return data