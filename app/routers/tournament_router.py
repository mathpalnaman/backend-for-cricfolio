# /app/routers/tournament_router.py
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Form,
    UploadFile,
    File,
    status,
    Request # Import Request
)
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import date

# Use the existing synchronous get_db dependency
from app.database.database import SessionLocal # Needed for get_db definition if not imported elsewhere
# Reuse the get_db function from contact router or define it here if preferred
# Let's assume it's defined accessibly, maybe move get_db to database.py?
# For now, copy the definition:
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from app.schemas.tournament_schema import TournamentRead # Response schema
from app.crud import tournament_crud # Import CRUD functions
from app.utils.file_utils import save_upload_file_sync # Sync file save

# Define where banners will be served from (relative to static files mount)
BANNER_URL_PREFIX = "/static/banners" # Ensure this matches main.py static mount

router = APIRouter(
    prefix="/tournaments", # Base path for this router
    tags=["Tournaments"],  # Tag for docs
)

@router.post(
    "/",
    response_model=TournamentRead,
    status_code=status.HTTP_201_CREATED
)
def register_tournament(
    request: Request, # Inject Request to build absolute URLs
    db: Session = Depends(get_db),
    # Match form field names exactly from frontend state (camelCase)
    # Use Form(...) for all fields because of multipart/form-data
    tournamentName: str = Form(...),
    state: str = Form(...),
    city: str = Form(...),
    stadiumPark: str = Form(...),
    organizerName: str = Form(...),
    startDate: date = Form(...),
    endDate: date = Form(...),
    category: str = Form(...),
    ballType: str = Form(...),
    matchStyle: str = Form(...),
    guidelines: Optional[str] = Form(None),
    banner: Optional[UploadFile] = File(None) # Corresponds to 'banner' in frontend formData
):
    """
    Registers a new tournament (synchronous).
    Receives data as multipart/form-data.
    """
    saved_banner_filename = None
    if banner:
        # Basic validation (can be expanded)
        if not banner.content_type.startswith("image/"):
             raise HTTPException(
                 status_code=status.HTTP_400_BAD_REQUEST,
                 detail="Banner must be an image file.",
             )
        saved_banner_filename = save_upload_file_sync(banner)
        if not saved_banner_filename:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Could not save tournament banner.",
            )

    # Prepare data for the database model (snake_case)
    # Map from camelCase (Form params) to snake_case (DB model)
    tournament_data_for_db = {
        "tournament_name": tournamentName,
        "state": state,
        "city": city,
        "stadium_park": stadiumPark,
        "organizer_name": organizerName,
        "start_date": startDate,
        "end_date": endDate,
        "category": category,
        "ball_type": ballType,
        "match_style": matchStyle,
        "guidelines": guidelines,
        "banner_filename": saved_banner_filename
    }

    try:
        created_tournament = tournament_crud.create_tournament(
            db=db, tournament_data=tournament_data_for_db
        )
    except Exception as e:
        # Log the error e
        print(f"Error creating tournament in DB: {e}")
        # Consider specific DB error handling (e.g., duplicate entry) if needed
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred while registering tournament.",
        )

    # Prepare the response using the Pydantic schema
    response_data = TournamentRead.model_validate(created_tournament, from_attributes=True).model_dump(by_alias=True)
    

    # Construct the full banner URL if a banner exists
    if created_tournament.banner_filename:
        base_url = str(request.base_url).rstrip('/')
        response_data["banner_url"] = f"{base_url}{BANNER_URL_PREFIX}/{created_tournament.banner_filename}"
    else:
        response_data["banner_url"] = None

    return response_data

@router.get(
    "/",
    response_model=List[TournamentRead],
    status_code=status.HTTP_200_OK
)
def get_tournaments(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of tournaments with pagination support.
    """
    tournaments = tournament_crud.get_tournaments(db, skip=skip, limit=limit)
    
    # Add banner URLs to each tournament
    response_data = []
    base_url = str(request.base_url).rstrip('/')
    
    for tournament in tournaments:
        tournament_data = TournamentRead.model_validate(tournament, from_attributes=True).model_dump(by_alias=True)
        if tournament.banner_filename:
            tournament_data["banner_url"] = f"{base_url}{BANNER_URL_PREFIX}/{tournament.banner_filename}"
        else:
            tournament_data["banner_url"] = None
        response_data.append(tournament_data)
    
    return response_data

@router.get(
    "/{tournament_id}",
    response_model=TournamentRead,
    status_code=status.HTTP_200_OK
)
def get_tournament(
    tournament_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific tournament by ID.
    """
    tournament = tournament_crud.get_tournament(db, tournament_id=tournament_id)
    if not tournament:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tournament with ID {tournament_id} not found"
        )
    
    # Prepare the response using the Pydantic schema
    response_data = TournamentRead.model_validate(tournament, from_attributes=True).model_dump(by_alias=True)
    
    # Add banner URL if exists
    if tournament.banner_filename:
        base_url = str(request.base_url).rstrip('/')
        response_data["banner_url"] = f"{base_url}{BANNER_URL_PREFIX}/{tournament.banner_filename}"
    else:
        response_data["banner_url"] = None
    
    return response_data