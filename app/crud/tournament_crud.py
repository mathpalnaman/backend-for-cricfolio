# /app/crud/tournament_crud.py
from sqlalchemy.orm import Session
from app.models.tournament_model import Tournament
from typing import Dict, Any

def create_tournament(db: Session, *, tournament_data: Dict[str, Any]) -> Tournament:
    """Creates a new tournament record using synchronous session."""
    # Map schema field names (like stadiumPark) to model field names (stadium_park)
    # This mapping happens implicitly if using **tournament_data if aliases match,
    # or you can do it explicitly. Let's assume aliases work via allow_population_by_field_name.
    # Ensure keys in tournament_data match the model's __init__ or column names.
    
    db_tournament = Tournament(**tournament_data)
    db.add(db_tournament)
    db.commit()
    db.refresh(db_tournament)
    return db_tournament

# Add other CRUD functions (get_tournament, get_tournaments, etc.) here later if needed