from sqlalchemy.orm import Session

import models, schemas


def get_burguer_by_id(db: Session, burguer_id: int):
    return db.query(models.Burguer).filter(models.Burguer.id == burguer_id).first()


def get_burguer_by_nombre(db: Session, nombre: str):
    return db.query(models.Burguer).filter(models.Burguer.nombre == nombre).first()

#he añadido esto:
def get_burguer_by_ingredientes(db: Session, ingredientes: str):
    return db.query(models.Burguer).filter(models.Burguer.ingredientes == ingredientes).first()



def get_burguers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Burguer).offset(skip).limit(limit).all()

def post_create_burguer(db: Session, burguer: schemas.Burguer):
    db_burguer = models.Burguer(
        nombre = burguer.nombre,
        ingredientes = burguer.ingredientes
        )
    db.add(db_burguer)
    db.commit()
    db.refresh(db_burguer)
    return db_burguer

#he añadido esto:
#Acabar:
def put_burguer_edit_burguer(db: Session, burguer: schemas.Burguer, burguerdelete: schemas.Burguer):
    '''db_burguer2 = models.Burguer(
        ingredientesextra = burguer.ingredientesextra,
        ingredientes = burguer.ingredientes,
        is_active = burguer.is_active,
        id = burguerdelete.id,
        nombre = burguerdelete.nombre
        )'''
    db.add(burguer)
    db.refresh(burguer)
    db.commit()
    return burguer

def delete_burguer(db: Session, burguer: schemas.Burguer):
    db.delete(burguer)
    db.commit()
    return db

def actualizar_ingredienetesextra(ingredienetesextra: str, db: Session, burguer: schemas.Burguer):
    burguer.ingredientesextra = ingredienetesextra
    db.refresh(burguer)
    db.commit()
    pass

"""
def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
"""
