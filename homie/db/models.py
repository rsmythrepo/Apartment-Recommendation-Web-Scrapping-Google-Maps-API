from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel


class PostalCode(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    code: str
    district: str | None

    services_collected: bool = Field(default=False)

    # metadata
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())

    flats: list["Flat"] = Relationship(back_populates="postal_code")
    services: list["Service"] = Relationship(back_populates="postal_code")


class Flat(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    title: str | None
    description: str | None

    # Metadata
    url: str | None
    published_at: datetime | None
    updated_at: datetime | None

    # Price
    price: float | None  # in euros
    price_per_m2: float | None  # in euros

    # Basic info
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

    # Building
    has_elevator: bool | None

    # Equipment
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

    # foreign key   
    postal_code_id: int | None = Field(default=None, foreign_key="postalcode.id")
    postal_code: PostalCode | None = Relationship(back_populates="flats")
    

    # metadata
    created_at: datetime = Field(default=datetime.now())
    source: str | None  # scrapper_name | file_type | {other_source}

    is_active: bool = Field(default=True)


class Service(SQLModel, table=True):
    """
    From Google Maps API.
    """
    id: int | None = Field(default=None, primary_key=True)

    name: str
    vicinity: str

    latitude: float
    longitude: float

    business_status: str
    rating: float
    user_ratings_total: int

    types: str
    original_type: str  # users search term

    # foreign key
    postal_code_id: int | None = Field(default=None, foreign_key="postalcode.id")
    postal_code: PostalCode | None = Relationship(back_populates="services")

    # metadata
    created_at: datetime = Field(default=datetime.now())
