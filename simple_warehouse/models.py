from sqlalchemy import Column, Integer, String, Float
# from sqlalchemy.orm import relationship

from .database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, unique=True, index=True)
    name = Column(String)
    price = Column(Float)
    tax = Column(Float)
    description = Column(String)