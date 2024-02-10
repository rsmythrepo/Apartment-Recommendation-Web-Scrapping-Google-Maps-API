import csv
import logging
import os
from datetime import datetime

from homie.db.models import Flat
from homie.db.session import db_session
from homie.db.queries import get_or_create_postal_code

logger = logging.getLogger("homie")


class CSVUploader:
    source = "csv"

    class Meta:
        model = None
        datetime_fields = []
        bool_fields = []
        float_fields = []
        int_fields = []

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
        pass

    def format_data(self, data):
        for field in self.Meta.datetime_fields:
            value = data.get(field)
            if value:
                data[field] = datetime.strptime(value, "%Y-%m-%d")
            else:
                data[field] = None

        for field in self.Meta.bool_fields:
            value = data.get(field)
            if value:
                data[field] = value.lower() == "true"
            else:
                data[field] = None

        for field in self.Meta.float_fields:
            value = data.get(field)
            if value:
                data[field] = float(value)
            else:
                data[field] = None

        for field in self.Meta.int_fields:
            value = data.get(field)
            if value:
                data[field] = int(value)
            else:
                data[field] = None

        return data


class FlatCSVUploader(CSVUploader):
    class Meta:
        model = Flat
        datetime_fields = ["published_at", "updated_at"]
        bool_fields = [
            "has_balcony", "has_heating", "allow_pets", "allow_kids",
            "exterior", "has_elevator", "has_air_conditioning",
            "has_energy_certification"
        ]
        float_fields = [
            "price", "price_per_m2", "energy_consumption", "energy_emissions"
        ]
        int_fields = ["space", "rooms", "bathrooms", "built_on", "max_guests"]

    @db_session
    def populate(self, file_path: str, session=None):
        objs_data = self.read_file(file_path)

        for data in objs_data:
            data = self.format_data(data)
            if not data.get("postal_code") and data.get("postal_code_str"):
                data["postal_code_id"] = get_or_create_postal_code(
                    data["postal_code_str"]
                ).id
            obj = Flat(**data, source=self.source)
            session.add(obj)
        session.commit()

        logger.info(f"{len(objs_data)} added")
