from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import funciones_api as fa
from typing import List


import importlib
importlib.reload(fa)
#importlib.reload(ML)

app = FastAPI() # Invocamos FastAPI


@app.get(path="/", 
         response_class=HTMLResponse,
         tags=["Home"])
def intro():
    '''
    Página de inicio que muestra una presentación.

    Returns:
    HTMLResponse: Respuesta HTML que muestra la presentación.
    '''
    return fa.intro()


# Desarrollador
@app.get("/developer/{desarrollador}", response_model=List, description=""" <font color="blue"> INSTRUCCIONES<br> 1. Haga clic en "Try it out".<br> 2. Ingrese el X en el cuadro de abajo.<br> 3. Desplácese hacia "Resposes" para ver `Cantidad` de items y `porcentaje` de contenido Free por año según empresa desarrolladora.<br> 4\_ Ejemplos de desarrolladores para consultar: Valve, Capcom </font> """, tags=["Consultas Generales"])
def developer(desarrollador: str):
    result = fa.developer(desarrollador)
    return result


@app.get("/userdata/{user_id}",response_model=List,  
            description="""
    <font color="blue">
        INSTRUCCIONES<br>
        1. Haga clic en "Try it out".<br>
        2. Ingrese el user_id en el cuadro de abajo.<br>
        3. Desplácese hacia "Resposes" para ver `cantidad` de dinero gastado por el usuario, el `porcentaje` de recomendación en base a reviews.recommend y `cantidad de juegos.<br>
        4_ Ejemplos de desarrolladores para consultar: evcentric, 76561198099295859
    </font>
""", 
tags=["Consultas Generales"])
def userdata(user_id: str):
    # Filtramos el DataFrame user_stats por el user_id
    result = fa.userdata(user_id)
    return result

# __________________________
# Definir punto final para la ruta '/recomendacion_juego/{user_id}'
@app.get('/recomendacion_juego/{user_id}')
def obtener_recomendaciones_usuario(user_id: str):
    # Llamar a la función recomendacion_juego del módulo funciones_api
    recomendaciones = fa.recomendacion_juego(user_id)
    return recomendaciones



'''
ME QUEDO PENDIENTE

# Función para el endpoint UserForGenre
@app.get("/UserForGenre/{genero}")
def UserForGenre(genero: str):
    # Código para procesar la consulta y devolver el resultado
    pass



# Función para el endpoint best_developer_year
@app.get("/best_developer_year/{año}")
def best_developer_year(año: int):
    # Código para procesar la consulta y devolver el resultado
    pass

'''

