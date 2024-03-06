from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel


class Flat(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    title: str | None
    description: str | None

    # metadata
    url: str | None
    published_at: datetime | None
    updated_at: datetime | None

    # price
    price: float | None  # in euros
    price_per_m2: float | None  # in euros

    # basic info
    space: int | None  # m2
    rooms: int | None
    bathrooms: int | None
    has_balcony: bool | None
    built_on: int | None  # year
    has_heating: bool | None
    heating_type: str | None
    allow_pets: bool | None
    allow_kids: bool | None
    max_guests: int | None
    exterior: bool | None
    has_air_conditioning: bool | None

    # energy certification
    has_energy_certification: bool | None
    energy_consumption: float | None  # kWh/m² per year
    energy_consumption_tag: str | None  # A | B | C | D | E | F | G
    energy_emissions: float | None  # kg CO2/m² per year
    energy_emissions_tag: str | None  # A | B | C | D | E | F | G

    # address
    postal_code_str: str | None
    district: str | None
    
    # from google maps api
    lat: float | None  # from gmaps
    lng: float | None  # from gmaps

    # metadata
    created_at: datetime = Field(default=datetime.now())
    source: str | None  # scrapper_name | file_type | {other_source}

    is_active: bool = Field(default=True)

    services_collected: bool = Field(default=False)

    @property
    def price_per_room(self) -> float:
        if not self.price or not self.rooms:
            return None
        return self.price / self.rooms


class Service(SQLModel, table=True):
    """
    From Google Maps API.
    """
    id: int | None = Field(default=None, primary_key=True)

    name: str
    formatted_address: str

    lat: float
    lng: float

    business_status: str
    rating: float
    user_ratings_total: int

    types: str
    original_type: str  # users search term

    flat_id: int | None = Field(default=None, foreign_key="flat.id")
    flat: Flat | None = Relationship(back_populates="services")

    # metadata
    created_at: datetime = Field(default=datetime.now())
