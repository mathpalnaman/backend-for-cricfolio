# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.database.database import SessionLocal
# from app.models.contact_model import Contact

# router = APIRouter()

# # Dependency to get DB session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @router.post("/contact")
# def submit_contact(name: str, phone: int, email: str, message: str, db: Session = Depends(get_db)):
#     contact_entry = Contact(name=name, phone=phone, email=email, message=message)
#     db.add(contact_entry)
#     db.commit()
#     db.refresh(contact_entry)
#     return {"message": "Contact saved successfully", "data": contact_entry.id}
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.models.contact_model import Contact
from pydantic import BaseModel, EmailStr

router = APIRouter()

# Pydantic model for input validation
class ContactSchema(BaseModel):
    name: str
    phone: int
    email: EmailStr
    message: str

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/contact")
def submit_contact(contact: ContactSchema, db: Session = Depends(get_db)):
    contact_entry = Contact(
        name=contact.name,
        phone=contact.phone,
        email=contact.email,
        message=contact.message
    )
    db.add(contact_entry)
    db.commit()
    db.refresh(contact_entry)
    return {"message": "Contact saved successfully", "id": contact_entry.id}
