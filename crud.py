from sqlalchemy.orm import Session

import models, schemas


def get_burguer_by_id(db: Session, burguer_id: int):
    return db.query(models.Burguer).filter(models.Burguer.id == burguer_id).first()


def get_burguer_by_nombre(db: Session, nombre: str):
    return db.query(models.Burguer).filter(models.Burguer.nombre == nombre).first()

#he añadido esto:
def get_burguer_by_ingredientes(db: Session, ingredientes: str):
    return db.query(models.Burguer).filter(models.Burguer.ingredientes == ingredientes).first()

def update_burguer_name(db: Session, burguer_id: int, newnombre: str):
    #db.query(models.Burguer).filter(models.Burguer.id == burguer_id).update(models.Burguer.nombre == newnombre)
    db.query(models.Burguer).update(models.Burguer.nombre == newnombre)
    db.commit()
    return db.query(models.Burguer).filter(models.Burguer.id == burguer_id)

'''def update_burguer_name(db: Session, burguer_id: int, newnombre: str):
    #db.query(models.Burguer).filter(models.Burguer.id == burguer_id).update(models.Burguer.nombre == newnombre)
    db.query(models.Burguer).update(models.Burguer.nombre == newnombre)
    db.commit()
    return db.query(models.Burguer).filter(models.Burguer.id == burguer_id)


def update_burguer_name2(db: Session, burguer_id: int, newnombre: str):
    #burguer = db.query(models.Burguer).filter(models.Burguer.id == burguer_id)
    burguer = get_burguer_by_id(db, burguer_id)
    burguer2 = burguer.copy()
    burguer2.se
    db.add(burguer2)
    db.commit()
    return db.query(models.Burguer).filter(models.Burguer.id == burguer_id)'''

'''def update_burguer_name3(db: Session, burguer: schemas.Burguer, newnombre : str):
    #burguer = db.query(models.Burguer).filter(models.Burguer.id == burguer_id)
    db.delete(burguer)
    db.add(burguer.set_name(newnombre))
    db.commit()
    return db.query(models.Burguer).filter(models.Burguer.id == burguer_id)'''

def update_burguer_name5(db: Session, newnombre : str, id: int):
    query="UPDATE burguers SET nombre = " + newnombre + " WHERE id= "+ str(id)
    db.execute(query)
    db.commit()
    return "consulta realizada"


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

def delete_burguer(db: Session, burguer: schemas.Burguer):
    db.delete(burguer)
    db.commit()
    return db

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
