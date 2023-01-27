# sintaxis: from carpeta.nombre_del_modulo import x
from endpoints import app 
'''
Para iniciar la API ejecutar en consola el comando:
uvicorn main:app --reload 

Hay que importar app para que cuando se ejecute el comando 
uvicorn main:app la app se detecte en el main (mapping)

Se encuentra en la direccion http://127.0.0.1:8000/
IMPORTANTE: Aquí esta la API http://127.0.0.1:8000/docs

Para ejecutar los test se ejecutara el siguiente comando:
pytest test.py
'''
#En este ejercicio todas las hamburguesas se llaman 
# "burguers", no burgers porque he querido.