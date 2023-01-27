from sqlalchemy.orm import Session
from fastapi import HTTPException
import models, schemas

'''POST'''
#POST crear hamburguesa recibiendo parámetros
def post_create_burguer_bien(db: Session,imagen: str, newnombre: str, newingredientes: str, active:int):
    db_burguer = models.Burguer()
    db_burguer.nombre=newnombre
    db_burguer.ingredientes=newingredientes
    db_burguer.imagen=imagen
    if active==0:
        db_burguer.is_active=False
    else:
        if active==1 or active==-1:
            db_burguer.is_active=True
        else:
            raise HTTPException(status_code=400, detail="El valor de active debe ser 0 (False), 1 (True) o -1(Default=True)")
    db.add(db_burguer)
    db.commit()
    #db.refresh(db_burguer)
    return db_burguer

#POST crear hamburguesa recibiendo un schema.Burguer
def post_create_burguer(db: Session, burguer: schemas.Burguer):
    db_burguer = models.Burguer(
        nombre = burguer.nombre,
        ingredientes = burguer.ingredientes
        )
    db.add(db_burguer)
    db.commit()
    db.refresh(db_burguer)
    return db_burguer


'''GET'''
#GET by id
def get_burguer_by_id(db: Session, burguer_id: int):
    return db.query(models.Burguer).filter(models.Burguer.id == burguer_id).first()
    
#GET img
def get_img(burguer: models.Burguer):
    return burguer.imagen

#GET by nombre
def get_burguer_by_nombre(db: Session, nombre: str):
    return db.query(models.Burguer).filter(models.Burguer.nombre == nombre).first()

#GET by ingredienetes
def get_burguer_by_ingredientes(db: Session, ingredientes: str):
    return db.query(models.Burguer).filter(models.Burguer.ingredientes == ingredientes).first()

#GET all
def get_burguers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Burguer).offset(skip).limit(limit).all()

# get ing by burguer
def get_ing(burguer: schemas.Burguer):
    return burguer.ingredientes

'''OPTIONS'''
def options_get_isactive(burguer:models.Burguer):
    return burguer.is_active

'''PUT'''
#PUT update name
def put_burguer2(db: Session, newnombre: str, burgueraeditar: schemas.Burguer):
    burgueraeditar.nombre = newnombre
    db.commit()
    return burgueraeditar

#PUT update name and ingredients
def put_burguer_name_and_ingredients(db: Session, burguer: schemas.Burguer, burguerborrada: schemas.Burguer):
    db_burguer = models.Burguer(
        nombre = burguer.nombre,
        ingredientes = burguer.ingredientes
        )
    db.delete(burguerborrada) #new
    #db_burguer.ingredientes =  burguerborrada.ingredientes
    db.add(db_burguer)
    db.commit()
    db.refresh(db_burguer)
    #db.delete(burguerborrada)
    db.commit()
    return db_burguer

#PUT update all
def put_burguer(db: Session, img: str, newnombre: str, newingredientes: str, newactive: int, burgueraeditar: schemas.Burguer):
    cambios =False
    if newactive==0:
        burgueraeditar.is_active=False
        cambios = True
    else:
        if newactive==1:
            burgueraeditar.is_active=True
            cambios = True
        else:
            if newactive != -1:
                raise HTTPException(status_code=400, detail="El valor de active debe ser 0 (False), 1 (True) o -1(Default)")
    if newnombre != "":
        burgueraeditar.nombre = newnombre
        cambios=True
    if newingredientes != "":
        burgueraeditar.ingredientes = newingredientes
        cambios=True
    if img != "":
        burgueraeditar.imagen = img
        cambios=True
    if cambios == False:
        raise HTTPException(status_code=400, detail="No se han introducido datos")
    db.commit()
    return burgueraeditar


'''DELETE'''
#DELETE burguer by id
def delete_burguer(db: Session, burguer: schemas.Burguer):
    db.delete(burguer)
    db.commit()
    return db
