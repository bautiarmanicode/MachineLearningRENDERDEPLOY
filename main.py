from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import funciones_api as fa
from funciones_api import developer
from typing import List

# import ML_itemxitem as ML



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
#
#
@app.get("/developer/{desarrollador}",response_model=List,  
            description="""
    <font color="blue">
        INSTRUCCIONES<br>
        1. Haga clic en "Try it out".<br>
        2. Ingrese el X en el cuadro de abajo.<br>
        3. Desplácese hacia "Resposes" para ver x que tiene el mismo.<br>
        4_ Ejemplos de desarrolladores para consultar: Valve, Capcom
    </font>
""", 
tags=["Consultas Generales"])

def developer(desarrollador: str):    
    resultadodesarrollador = fa.developer(desarrollador)
    return resultadodesarrollador


@app.get("/userdata/{user_id}",response_model=List,  
            description="""
    <font color="blue">
        INSTRUCCIONES<br>
        1. Haga clic en "Try it out".<br>
        2. Ingrese el X en el cuadro de abajo.<br>
        3. Desplácese hacia "Resposes" para ver x que tiene el mismo.<br>
        4_ Ejemplos de desarrolladores para consultar: Valve, Capcom
    </font>
""", 
tags=["Consultas Generales"])

def userdata(user_id: str):    
    user = fa.userdata(user_id)
    return user