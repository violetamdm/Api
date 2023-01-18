#fastapi:
'''Instalado fastapi y Uvicorn con pip'''
#comando para empezar la API: uvicorn main:app --reload
#import asyncio
#import datetime
#import requests
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from fastapi import Body
#crear archivo .gitignore
app = FastAPI()
#orm
class Burguer(BaseModel):
     id: int 
     nombre: str
     ingredientes: str
     ingredientesextra: str

#llamada al home de la API
@app.get("/")  
def home():  
	 return { "mensaje" : "Esta es la raíz de la app bienvenido" }

#llamada para crear una nueva burguer
@app.post("/burguers/{burguer_id}")
def create_burguers(burguer_id: int, burguers: Burguer = Body(...)): 
    return {burguer_id: int, burguers:Burguer}

""" 
ejemplo burguer creada con éxito (no se guardan los datos mas allá del id):
{
  "id": 0,
  "nombre": "cheseburguer",
  "ingredientes": "meat, cheese",
  "ingredientesextra": "ketchup"
}
"""
# Si este post (anterior) no funciona probar copn esto:
'''
#llamada para crear una nueva burguer
@app.post("/burguers/{burguer_id}")
def create_burguerprueba(
         burguer_id: int, 
		 q: Optional[str] = None,
         ingredientes: Optional[str] = None,
         extra: Optional[str] = None):
     return {"item_id": burguer_id, "q": q, "ingredientes": ingredientes, "extra": extra}
'''

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

class TryTesting(TestCase):
    def test_always_passes(self):
        self.assertTrue(True)

    def test_always_fails(self):
        self.assertTrue(False)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}

#Por consola:
# python -m unittest discover