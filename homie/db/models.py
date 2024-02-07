from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import Optional, List


class Flat(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: Optional[str]
    description: Optional[str]
    price: Optional[float]
    published_at: Optional[datetime]

    address: Optional[str]
    latitude: Optional[float]  # from gmaps
    longitude: Optional[float]  # from gmaps

    # todo: @raph
    
    # metadata
    created_at: datetime = Field(default=datetime.now())
    services_collected: bool = Field(default=False)  # google maps api

    is_active: bool = Field(default=True)

    # relationships
    services: List["FlatService"] = Relationship(back_populates="flat")

    def add_lat_lng(self, lat, lng):
        self.latitude = lat
        self.longitude = lng
        self.services_collected = True


class FlatService(SQLModel, table=True):
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
