from pydantic import BaseModel
"""
class ItemBase(BaseModel):
    title: str
    description: Union[str, None] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
"""

class Burguer(BaseModel):
    #identificador_interno: int
    id: int
    is_active: bool
    ingredientes: str
    nombre: str
    imagen: str
    class Config:
        orm_mode = True