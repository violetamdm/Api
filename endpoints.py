from typing import List
from fastapi import Depends, FastAPI, HTTPException, status
from PIL import Image
from sqlalchemy.orm import Session
import schemas
from database import SessionLocal
import crud  # con esto hay que poner el crud.nombrefuncion
#from crud import * #esto importa todas las funciones de crud
from fastapi.responses import FileResponse, RedirectResponse

app = FastAPI()

# crear la sesion de la bbdd:
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


'''GET'''

#GET que redirige a /docs desde la raiz del proyecto
@app.get("/")
async def redirect_typer():
    return RedirectResponse("http://127.0.0.1:8000/docs")

#ejemplo de get
@app.get("/home", status_code=status.HTTP_200_OK)  
def home():  
	 return { "mensaje" : "Usted se encuentra en la /home de la app bienvenido" }

#GET lista de burguers
@app.get("/burguers/", response_model=List[schemas.Burguer], status_code=status.HTTP_200_OK)
def get_burguers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    burguers = crud.get_burguers(db, skip=skip, limit=limit)
    return burguers

#GET abre la imagen burguer
@app.get("/burguers/showimages", status_code=status.HTTP_200_OK)
def get_burguers(id: int = 0, db: Session = Depends(get_db)):
    burguer = crud.get_burguer_by_id(db, id)
    strimg = crud.get_img(burguer)
    img = Image.open(strimg)
    img.show()
    return  { "stringimagen" : strimg } 

#GET muestra una imagen como respuesta
@app.get("/burguers/showimages2", response_class=FileResponse)
async def get_img(id: int = 0, db: Session = Depends(get_db)):
    burguer = crud.get_burguer_by_id(db, id)
    strimg = crud.get_img(burguer)
    return strimg

#GET lista de las imagenes que tienen mis burguers, pueden estar repetidas 
# no son las que hay pueden existir mas y no estar en uso
@app.get("/burguers/imgs", status_code=status.HTTP_200_OK)
def get_obtener_las_imagenes_de_mis_burguers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    burguers = crud.get_burguers(db, skip=skip, limit=limit)
    strimgs = ""
    y=0
    for x in burguers :
        if y==0:
            strimgs = crud.get_img(x)
            y = 1
        else: 
            strimgs = strimgs + ", " + crud.get_img(x)
    return {"Imagenes": strimgs}


#GET by id
@app.get("/burguers/{burguer_id}", response_model=schemas.Burguer, status_code=status.HTTP_200_OK)
def burguer_by_id(burguer_id: int, db: Session = Depends(get_db)):
    db_burguer = crud.get_burguer_by_id(db, burguer_id=burguer_id)
    if db_burguer is None:
        raise HTTPException(status_code=404, detail="Burguer not found")
    return db_burguer

'''POST'''
#llamada para crear una nueva burguer
@app.post("/burguers/", response_model=schemas.Burguer, status_code=status.HTTP_200_OK)
def create_burguer_bien(
    nombre: str, 
    ingredientes: str, 
    active: int = -1,
    imagen: str ="b.jpg",
    db: Session = Depends(get_db)
    ):  
    if nombre=="" or ingredientes=="":
        raise HTTPException(status_code=400, detail=" El nombre y/o los ingredientes no pueden ser vacíos")
    db_burguer = crud.get_burguer_by_nombre(db, nombre)
    db_burguer2 = crud.get_burguer_by_ingredientes(db, ingredientes)
    if db_burguer:
        raise HTTPException(status_code=400, detail="Nombre already registered")
    else: 
        if db_burguer2:
            raise HTTPException(status_code=400, detail="Other burguer have the same ingredients")
    return crud.post_create_burguer_bien(db=db, imagen=imagen, newnombre=nombre, newingredientes=ingredientes, active=active)
'''OPTIONS'''
#OPTIONS opciones de comunicación para el 
# recurso de destino.
@app.options("/")
async def options_isactive(burguer_id: int, db: Session = Depends(get_db)):
    burguer = crud.get_burguer_by_id(db, burguer_id)
    if burguer == None:
        raise HTTPException(status_code=404, detail="Burguer not found (this id is not here)")
    active = crud.options_get_isactive(burguer).__str__()
    return {"message": active}

'''PUT'''
#llamada para cualquier item de burguers. 
@app.put("/burguers/{burguer_id}", response_model=schemas.Burguer, status_code=status.HTTP_200_OK)
def update_burguer_items(burguer_id: int,
    newnombre: str = "", 
    ingredientes: str = "",
    Active: int = -1,
    imagen: str="b.jpg",
    db: Session = Depends(get_db)
    ):  
    burgueraeditar = crud.get_burguer_by_id(db, burguer_id)
    db_burguer = crud.get_burguer_by_nombre(db, nombre=newnombre)
    if db_burguer:
        raise HTTPException(status_code=400, detail="Nombre already registered")
    else: 
        if burgueraeditar == None:
            raise HTTPException(status_code=400, detail="Id not found")
    return crud.put_burguer(db=db, img = imagen, newnombre=newnombre, newingredientes=ingredientes, burgueraeditar=burgueraeditar, newactive=Active)

#put para editar nombre solamente
@app.put("/burguers/", response_model=schemas.Burguer, status_code=status.HTTP_200_OK)
def update_burguer_nombre(burguer_id: int,
    newnombre: str,  
    db: Session = Depends(get_db)
    ):  
    burgueraeditar = crud.get_burguer_by_id(db, burguer_id)
    db_burguer = crud.get_burguer_by_nombre(db, nombre=newnombre)
    if db_burguer:
        raise HTTPException(status_code=400, detail="Nombre already registered")
    else: 
        if burgueraeditar == None:
            raise HTTPException(status_code=400, detail="Id not found")
    return crud.put_burguer2(db=db, newnombre=newnombre, burgueraeditar=burgueraeditar)


#PUT mal hecho primero borra y luego crea uno nuevo, no edita
'''@app.put("/burguers/", response_model=schemas.Burguer, status_code=status.HTTP_200_OK)
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
    '''

'''DELETE'''
#DELETE para eliminar un recurso del servidor
@app.delete("/burguers/{burguer_id}", response_model=schemas.Burguer, status_code=status.HTTP_200_OK)
def prueba_delete_by_id(burguer_id: int, db: Session = Depends(get_db)):
    burguer=crud.get_burguer_by_id(db, burguer_id)
    return  crud.delete_burguer(db, burguer)
    
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
