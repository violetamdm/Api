#fastapi:
'''Instalado fastapi y Uvicorn con pip'''

'''
para iniciar la api poner en consola:
uvicorn main:app --reload 

se encuentra en la direccion http://127.0.0.1:8000/
IMPORTANTE: Aquí esta la API http://127.0.0.1:8000/docs
'''
#comando para empezar la API: uvicorn main:app --reload
#import asyncio
#import datetime
#import requests
from ast import Dict
from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine
import schemas
from fastapi import status
from typing import  List
from fastapi.testclient import TestClient
from fastapi import APIRouter

from fastapi import APIRouter, Query, status
from pydantic import Required
from typing import Dict, List


router =  APIRouter()

client = TestClient(router)

models.Base.metadata.create_all(bind=engine)
#crear archivo .gitignore

#En este ejercicio todas las hamburguesas se llaman 
# "burguers", no burgers porque he querido.

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#llamada al home de la API
@app.get("/", status_code=status.HTTP_200_OK)  
def home():  
	 return { "mensaje" : "Esta es la raíz de la app bienvenido" }

'''
#llamada para actualizar un item en específico. 
@app.put("/burguers/{burguer_id}", response_model=schemas.Burguer)
def update_burguer(burguer_id: int, db: Session = Depends(get_db)):
    db_burguer = crud.get_burguer_by_id(db, burguer_id=burguer_id)
    return crud.put_burguer_edit_burguer(db, db_burguer) 
'''

@app.get("/burguers/", response_model=List[schemas.Burguer], status_code=status.HTTP_200_OK)
def get_burguers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    burguers = crud.get_burguers(db, skip=skip, limit=limit)
    return burguers

@app.get("/burguers/{burguer_id}", response_model=schemas.Burguer, status_code=status.HTTP_200_OK)
def burguer_by_id(burguer_id: int, db: Session = Depends(get_db)):
    db_burguer = crud.get_burguer_by_id(db, burguer_id=burguer_id)
    if db_burguer is None:
        raise HTTPException(status_code=404, detail="Burguer not found")
    return db_burguer

#DELETE para eliminar un recurso del servidor
@app.delete("/burguers/{burguer_id}")
def prueba_delete_by_id(burguer_id: int, db: Session = Depends(get_db), status_code=status.HTTP_200_OK):
    burguer=crud.get_burguer_by_id(db, burguer_id)
    return  crud.delete_burguer(db, burguer)

#llamada para crear una nueva burguer
@app.post("/burguers/", response_model=schemas.Burguer, status_code=status.HTTP_200_OK)
def create_burguer(
    burguer: schemas.Burguer,  
    db: Session = Depends(get_db)
    ):  
    db_burguer = crud.get_burguer_by_nombre(db, nombre=burguer.nombre)
    db_burguer2 = crud.get_burguer_by_ingredientes(db, ingredientes=burguer.ingredientes)
    if db_burguer:
        raise HTTPException(status_code=400, detail="Nombre already registered")
    else: 
        if db_burguer2:
            raise HTTPException(status_code=400, detail="Other burguer have the same ingredients")
    return crud.post_create_burguer(db=db, burguer=burguer)

'''#response_model=schemas.Burguer
@app.put("/burguers/", status_code=status.HTTP_200_OK)
def update_burguer(burguer_id: int, nombrenuevo: str, db: Session = Depends(get_db)):
    db_burguer = crud.get_burguer_by_nombre(db, nombrenuevo)
    if db_burguer:
        raise HTTPException(status_code=400, detail="Nombre already registered")
    return  crud.update_burguer_name5(db, nombrenuevo, burguer_id)'''

@app.put("/burguers/", response_model=schemas.Burguer, status_code=status.HTTP_200_OK)
def update_burguer_nombre_and_ingredientes(burguer_id: int,
    burguer: schemas.Burguer,  
    db: Session = Depends(get_db)
    ):  
    burguerborrar = crud.get_burguer_by_id(db, burguer_id)
    db_burguer = crud.get_burguer_by_nombre(db, nombre=burguer.nombre)
    db_burguer2 = crud.get_burguer_by_ingredientes(db, ingredientes=burguer.ingredientes)
    if db_burguer:
        raise HTTPException(status_code=400, detail="Nombre already registered")
    else: 
        if db_burguer2:
            raise HTTPException(status_code=400, detail="Other burguer have the same ingredients")
    return crud.put_burguer_name_and_ingredients(db=db, burguer=burguer, burguerborrada=burguerborrar)

# Ejemplos de endpoints:
'''
#POST para crear un recurso del servidor
#llamada para crear un nuevo item

@app.post("/recursos/{recurso_id}")
async def prueba_post_crear_item(recurso_id: int,  q: Optional[str]=None):
    results = {"recurso_id": recurso_id, "q": q}
    return results # + {"message": "se ha registrado una hamburguesa"}

#OPTIONS opciones de comunicación para el 
# recurso de destino.
@app.options("/")
async def prueba_options(id):
    return {"message": "esto es una prueba"}

#PUT para actualizar un recurso del servidor
@app.put("/")
async def prueba_put(id):
    return {"message": "esto es una prueba"}

#PATCH hace modificaciones parciales a un recurso.
@app.patch("/")
async def prueba_patch(id):
    return {"message": "esto es una prueba"}

#GET para obtener un recurso del servidor
@app.get("/recursos/{recurso_id}")
async def prueba_get(recurso_id: int, q: Optional[str]=None):
    results = {"recurso_id" : recurso_id, "q" : q}
    return results

#DELETE para eliminar un recurso del servidor
@app.delete("/")
async def prueba_delete(id):
    return {"message": "esto es una prueba"}

#TRACE  realizar una prueba de bucle invertido
#de mensajes que prueba la ruta del recurso 
# e destino (útil para fines de depuración).
@app.trace("/")
async def prueba_trace(id):
    return {"message": "esto es una prueba"}

'''
#pytest
from unittest import TestCase
from fastapi.testclient import TestClient

'''client = TestClient(app)'''

#pytest main.py
'''
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == { "mensaje" : "Esta es la raíz de la app bienvenido" }'''

class TryTesting(TestCase):
    def test_always_passes(self):
        self.assertTrue(True)

    '''def test_always_fails(self):
        self.assertTrue(False)'''

def test_get_home_connection():
    assert home() ==  { "mensaje" : "Esta es la raíz de la app bienvenido" }

def test_database_burguer():
    burgueraux = {
            "id": 1,
            "is_active": False,
            "ingredientes": "ole",
            "ingredientesextra":"ello",
            "nombre": "sudo"
            }
    newbur =  schemas.Burguer(id=1,is_active=False,ingredientes="ole", ingredientesextra="ello", nombre="sudo")
    assert newbur == burgueraux
#intentos fallidos:
"""
def test_get_by_title():
    response = client.get("/burguers/1")
    assert response.status_code == 200

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}"""

###############################################################################################

#Por consola:
# ir a proyectos\Api
#Ejecutar comando: 
# pytest main.py