from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import Optional, List
from db.session import db_session


class Generic:
    @db_session
    def save(self, session) -> None:
        """
        Save the data into the db
        """
        session.add(self)
        session.commit()


class Flat(Generic, SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    title: Optional[str]
    description: Optional[str]    

    # Metadata
    url = Optional[str]
    published_at: Optional[datetime]
    updated_at: Optional[datetime]

    # Price
    price = Optional[float]  # in euros
    price_per_m2 = Optional[float]  # in euros

    # Basic info
    space = Optional[int]  # m2
    rooms = Optional[int]
    bathrooms = Optional[int]
    has_balcony = Optional[bool]
    built_on = Optional[int]  # year
    has_heating = Optional[bool]
    heating_type = Optional[str]
    allow_pets = Optional[bool]
    allow_kids = Optional[bool]
    allow_kids = Optional[bool]
    max_guests = Optional[int]
    exterior = Optional[bool]

    # Building
    has_elevator = Optional[bool]

    # Equipment
    has_air_conditioning = Optional[bool]

    # energy certification
    has_energy_certification = Optional[bool]
    energy_consumption = Optional[float]  # kWh/m² per year
    energy_consumption_tag = Optional[str]  # A | B | C | D | E | F | G
    energy_emissions = Optional[float]  # kg CO2/m² per year
    energy_emissions_tag = Optional[str]  # A | B | C | D | E | F | G

    address: Optional[str]

    # todo: @raph
    
    # metadata
    created_at: datetime = Field(default=datetime.now())
    services_collected: bool = Field(default=False)  # google maps api
    source = Optional[str]  # scrapper_name | file_type | {other_source}

    is_active: bool = Field(default=True)

    # from google maps api
    latitude: Optional[float]  # from gmaps
    longitude: Optional[float]  # from gmaps

    # relationships
    services: List["FlatService"] = Relationship(back_populates="flat")

    def add_lat_lng(self, lat: float, lng: float) -> None:
        self.latitude = lat
        self.longitude = lng
        self.services_collected = True

    @db_session
    def save_multiple(self, session, flats: List["Flat"]) -> None:
        """
        Save multiple flats
        """
        # todo: check for repeated flats
        for flat in flats:
            session.add(flat)
        session.commit()


class FlatService(Generic, SQLModel, table=True):
    """
    From Google Maps API.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    
    name: str
    vicinity: str

    latitude: float
    longitude: float

    business_status: str
    rating: float
    user_ratings_total: int

    types: str
    original_type: str

    # relationships
    flat_id: Optional[int] = Field(default=None, foreign_key="flat.id")
    flat: Optional[Flat] = Relationship(back_populates="services")

    # metadata
    created_at: datetime = Field(default=datetime.now())
