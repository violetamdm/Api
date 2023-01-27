import models
from database import engine
import schemas
from endpoints import home, create_burguer_bien
from fastapi.testclient import TestClient
from fastapi import APIRouter
from unittest import TestCase
from fastapi.testclient import TestClient
from database import SessionLocal
#Por consola:
# ir a proyectos\Api
#Ejecutar comando: 
# pytest main.py
# (checkear si existe)

router =  APIRouter()
client = TestClient(router)
models.Base.metadata.create_all(bind=engine)

class TryTesting(TestCase):
    def test_always_passes(self):
        self.assertTrue(True)

def test_get_home_connection():
    assert home() ==  { "mensaje" : "Usted se encuentra en la /home de la app bienvenido" }

def test_post():
    db = SessionLocal()
    burgueraux = schemas.Burguer(id=1,is_active=False,ingredientes="ole", nombre="sudo", imagen="b.jpg")
    burgueraux2 = create_burguer_bien("sudo", "ole",0,"b.jpg", db)
    assert  burgueraux2.nombre == burgueraux.nombre
    assert  burgueraux2.ingredientes == burgueraux.ingredientes
    assert  burgueraux2.imagen == burgueraux.imagen
    assert  burgueraux2.is_active == burgueraux.is_active

'''def test_get_img_connection():
    db  = SessionLocal()
    b = crud.get_burguer_by_id(burguer_id=1, db=db)
    i = crud.get_img(b)
    assert get_img(1, db) == open(i, "r")'''

def test_database_burguer():
    burgueraux = {
            "id": 1,
            "is_active": False,
            "ingredientes": "ole",
            "nombre": "sudo", 
            "imagen": "b.jpg"
            }
    newbur = schemas.Burguer(id=1,is_active=False,ingredientes="ole", nombre="sudo", imagen="b.jpg")
    assert newbur == burgueraux

#ARREGLAR
'''def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == { "mensaje" : "Esta es la raíz de la app bienvenido" }'''

#intentos fallidos:
"""
def test_get_by_title():
    response = client.get("/burguers/1")
    assert response.status_code == 200

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}"""