#fastapi:
'''Instalado fastapi y Uvicorn con pip'''
#comando para empezar la API: uvicorn main:app --reload
#import asyncio
#import datetime
#import requests
from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine
from pydantic import BaseModel
import schemas
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
@app.get("/")  
def home():  
	 return { "mensaje" : "Esta es la raíz de la app bienvenido" }

'''
#llamada para actualizar un item en específico. 
@app.put("/burguers/{burguer_id}", response_model=schemas.Burguer)
def update_burguer(burguer_id: int, db: Session = Depends(get_db)):
    db_burguer = crud.get_burguer_by_id(db, burguer_id=burguer_id)
    return crud.put_burguer_edit_burguer(db, db_burguer) 
'''

@app.get("/burguers/", response_model=List[schemas.Burguer])
def get_burguers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    burguers = crud.get_burguers(db, skip=skip, limit=limit)
    return burguers

@app.get("/burguers/{burguer_id}", response_model=schemas.Burguer)
def burguer_by_id(burguer_id: int, db: Session = Depends(get_db)):
    db_burguer = crud.get_burguer_by_id(db, burguer_id=burguer_id)
    if db_burguer is None:
        raise HTTPException(status_code=404, detail="Burguer not found")
    return db_burguer

#DELETE para eliminar un recurso del servidor
@app.delete("/burguers/{burguer_id}")
def prueba_delete_by_id(burguer_id: int, db: Session = Depends(get_db)):
    burguer=crud.get_burguer_by_id(db, burguer_id)
    return  crud.delete_burguer(db, burguer)

#llamada para crear una nueva burguer
@app.post("/burguers/", response_model=schemas.Burguer)
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

"""@app.put("/burguers/",  response_model=schemas.Burguer)
def update_burguer(burguer: schemas.Burguer , burguer_id: int, db: Session = Depends(get_db)):
    db_burguer = crud.get_burguer_by_nombre(db, nombre=burguer.nombre)
    '''db_burguer2 = crud.get_burguer_by_ingredientes(db, ingredientes=burguer.ingredientes)
    if db_burguer:
        raise HTTPException(status_code=400, detail="Nombre already registered")
    else: 
        if db_burguer2:
            raise HTTPException(status_code=400, detail="Other burguer have the same ingredients")
    db_burguer = crud.get_burguer_by_id(db, burguer_id)'''
    crud.delete_burguer(db, db_burguer, burguer_id)
    crud.post_create_burguer(db, burguer)
    return  "se hizo un put

    
@app.put("/burguers/",  response_model=schemas.Burguer)
def update_burguer(ingredientesextra: schemas.Burguer.ingredientesextra , burguer_id: int, db: Session = Depends(get_db)):
    db_burguer = crud.get_burguer_by_id(db, burguer_id)
    crud.actualizar_ingredienetesextra(ingredientesextra, db, db_burguer)
    return  "se hizo un put"
    #return crud.put_burguer_edit_burguer(db, burguer, db_burguer)
    """

#################### Esto lo hice antes de la bbdd: ########################
"""
#llamada que va path burguers y que tome el burguer_id que estamos pasando como parametro
@app.get("/burguers/{burguer_id}")
def get_burguer( 
		 burguer_id: int, 
		 q: Optional[str] = None,
         ingredientes: Optional[str] = None,
         extra: Optional[str] = None):
     return {"item_id": burguer_id, "q": q, "ingredientes": ingredientes, "extra": extra}

@app.get("/burguers/{burguer_id}")
def get_burguerprueba(burguer_id: int):
     return {"item_id": burguer_id}

#llamada para actualizar un item en específico. 
@app.put("/burguers/{burguer_id}")
def update_item(burguer_id: int, burguer: Burguer):
    return {"item_name": burguer.nombre, "item_id": burguer_id}

#DELETE para eliminar un recurso del servidor
@app.delete("/burguers/{burguer_id}")
async def prueba_delete(burguer_id: int, burguer: Burguer):
    return  {"item_name": burguer.nombre}
"""
########################################
"""
'''asyncio is used as a foundation for multiple Python 
asynchronous frameworks that provide high-performance 
network and web-servers, database connection libraries, 
distributed task queues, etc.'''
# asyncio.sleep(1) # duerme 1 second

''' Asíncrono es "concurencia" (se usa todo
lo disponible: busca ser lo mas eficiente posible
todo el ratos, si tienes que esperar estas ocioso, 
asique mientras no se ocupan recursos se usan para
otra cosa) para cuando no hay q sincronizar 
nada, es decir no hay que esperar una respuesta de ningun sitio
en este caso son ejemplos y no hay que comunicarse con un 
servidor "async def" también se usa await'''
###################################################################
'''await tiene que estar dentro de una funcion async def'''
"""
'''
async def get_burguers(burguers: int):  
    await asyncio.sleep(1)
    return {burguers}

burgers = get_burguers(2)
print("hay " + burgers + "burguers")
'''
''' Síncrono es cuando hay que esperar respuestas y se usa 
solo "def" '''

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

#Es un GET sin el cuerpo de respuesta ???
@app.head("/")
async def prueba_head(id):
    return {"message": "esto es una prueba"}

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
#connect¿¿¿???
'''
para iniciar la api poner en consola:
uvicorn main:app --reload 

se encuentra en la direccion http://127.0.0.1:8000/
IMPORTANTE: Aquí esta la API http://127.0.0.1:8000/docs
'''
#pytest
from unittest import TestCase
'''from fastapi.testclient import TestClient'''

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

def test_get_home():
    assert home() ==  { "mensaje" : "Esta es la raíz de la app bienvenido" }

'''def test_get_all():
    response = client.get("/burguers")
    assert response.status_code == 200
    #assert response.json()'''

'''
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
'''
#Por consola:
# python -m unittest discover