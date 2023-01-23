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
    id: int
    is_active: bool
    ingredientes: str
    ingredientesextra: str
    nombre: str
    class Config:
        orm_mode = True

