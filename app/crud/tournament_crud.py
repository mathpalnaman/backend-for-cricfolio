# /app/crud/tournament_crud.py
from sqlalchemy.orm import Session
from app.models.tournament_model import Tournament
from typing import Dict, Any, List, Optional

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

def get_tournaments(db: Session, skip: int = 0, limit: int = 100) -> List[Tournament]:
    """
    Retrieve a list of tournaments with pagination support.
    
    Args:
        db: Database session
        skip: Number of records to skip (offset)
        limit: Maximum number of records to return
    
    Returns:
        List of Tournament objects
    """
    return db.query(Tournament).order_by(Tournament.created_at.desc()).offset(skip).limit(limit).all()

def get_tournament(db: Session, tournament_id: int) -> Optional[Tournament]:
    """
    Retrieve a specific tournament by ID.
    
    Args:
        db: Database session
        tournament_id: ID of the tournament to retrieve
    
    Returns:
        Tournament object if found, None otherwise
    """
    return db.query(Tournament).filter(Tournament.id == tournament_id).first()

# Add other CRUD functions (get_tournament, get_tournaments, etc.) here later if needed