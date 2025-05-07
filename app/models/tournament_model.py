# /app/models/tournament_model.py
from sqlalchemy import Column, Integer, String, Date, Text, TIMESTAMP, func
from app.database.database import Base # Use the existing Base
from datetime import date as DateType # Alias to avoid conflict with column type

class Tournament(Base):
    __tablename__ = "tournaments" # Use plural table name by convention

    id = Column(Integer, primary_key=True, index=True)
    tournament_name = Column(String, nullable=False, index=True)
    state = Column(String, nullable=False)
    city = Column(String, nullable=False)
    stadium_park = Column(String, nullable=False) # Changed from stadiumPark
    organizer_name = Column(String, nullable=False) # Changed from organizerName
    start_date = Column(Date, nullable=False) # Changed from startDate
    end_date = Column(Date, nullable=False)   # Changed from endDate
    category = Column(String, nullable=False)
    ball_type = Column(String, nullable=False) # Changed from ballType
    match_style = Column(String, nullable=False) # Changed from matchStyle
    guidelines = Column(Text, nullable=True)
    banner_filename = Column(String, nullable=True) # Store filename or path
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self):
        return f"<Tournament(name='{self.tournament_name}')>"