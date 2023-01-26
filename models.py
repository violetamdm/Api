from sqlalchemy import Boolean, Column, Integer, String
from database import Base

class Burguer(Base):
    __tablename__ = "burguers"
    #identificador_interno=Column(Integer, primary_key=True, index=True)
    id = Column(Integer,primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    ingredientes = Column(String, unique=True, index=True)
    is_active = Column(Boolean, unique=False)
    imagen = Column(String, unique=False)
    #items = relationship("Item", back_populates="owner")
    ## setter method to change the value 'a' using an object


"""
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
    """