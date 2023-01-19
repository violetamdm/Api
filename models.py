from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Burguer(Base):
    __tablename__ = "burguers"
     
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    ingredientes = Column(String, unique=True, index=True)
    ingredientesextra = Column(String, unique=False, index=True)
    is_active = Column(Boolean, default=True)
    #items = relationship("Item", back_populates="owner")

"""
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
    """