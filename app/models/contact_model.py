from sqlalchemy import Column, Integer, String, BigInteger
from app.database.database import Base

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(BigInteger, unique=True, nullable=False)  # Use BigInteger for large numbers
    email = Column(String, unique=True, nullable=False)
    message = Column(String, nullable=False)
