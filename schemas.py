from typing import List, Union

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


class BurguerBase(BaseModel):
    nombre: str


class BurguerCreate(BurguerBase):
    ingredientes: str
    ingredientesextra: str




class Burguer(BurguerBase):
    id: int
    is_active: bool
    #ingredientesextra: str
    #No sé para que es esto:
    class Config:
        orm_mode = True