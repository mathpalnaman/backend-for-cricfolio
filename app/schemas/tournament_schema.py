# /app/schemas/tournament_schema.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime

# Base schema with common fields, aligning with frontend state names
class TournamentBase(BaseModel):
    tournamentName: str = Field(..., alias="tournament_name") # Use alias for mapping if needed
    state: str
    city: str
    stadiumPark: str = Field(..., alias="stadium_park")
    organizerName: str = Field(..., alias="organizer_name")
    startDate: date = Field(..., alias="start_date")
    endDate: date = Field(..., alias="end_date")
    category: str
    ballType: str = Field(..., alias="ball_type")
    matchStyle: str = Field(..., alias="match_style")
    guidelines: Optional[str] = None

    class Config:
        orm_mode = True # To read data from ORM models
        allow_population_by_field_name = True # Allows using aliases

# Schema for reading data (response model)
class TournamentRead(TournamentBase):
    id: int
    banner_url: Optional[str] = None # URL will be constructed in the endpoint
    created_at: datetime