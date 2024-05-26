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


@app.get("/userdata/{user_id}", response_model=List,  
            description="""
    <font color="blue">
        ¡Bienvenido a la consulta de datos de usuario!<br>
        Siga estos pasos para obtener la información deseada:<br>
        1. Haga clic en "Try it out".<br>
        2. Ingrese el ID de usuario en el cuadro de abajo.<br>
        3. Desplácese hacia "Responses" para ver la cantidad de dinero gastado por el usuario, el porcentaje de recomendación basado en las reviews y la cantidad de juegos.<br>
        4. Ejemplos de ID de usuario para consultar: evcentric, 76561198099295859
    </font>
""", 
tags=["Consultas Generales"])
def userdata(user_id: str):
    """
    Devuelve la cantidad de dinero gastado por el usuario ingresado, el porcentaje de recomendación sobre las reviews realizadas y la cantidad de items.
    Ejemplo de retorno: [{"Usuario": "X", "Dinero gastado": "200 USD", "% de recomendación": "20%", "Cantidad de items": 5}]
    """
    # Filtramos el DataFrame user_stats por el user_id
    result = fa.userdata(user_id)
    return [result]  # Devuelve el diccionario dentro de una lista

# __________________________
# Definir punto final para la ruta '/recomendacion_juego/{user_id}'
# __________________________
# Definir punto final para la ruta '/recomendacion_juego/{user_id}'
@app.get('/recomendacion_juego/{user_id}', 
         description="""
    <font color="blue">
        ¡Bienvenido a la sección de recomendaciones de juegos!<br>
        Siga estos pasos para obtener las recomendaciones personalizadas:<br>
        1. Haga clic en "Try it out".<br>
        2. Ingrese el ID de usuario en el cuadro de abajo.<br>
        3. Desplácese hacia "Responses" para ver las 5 recomendaciones de juegos más adecuadas para el usuario.<br>
        4. ¡Disfruta explorando nuevos juegos!<br>
        Ejemplos de ID de usuario para probar: us213ndjss09sdf, evcentric, 76561198099295859
    </font>
""")
def obtener_recomendaciones_usuario(user_id: str):
    """
    Devuelve una lista con 5 recomendaciones de juegos para el usuario ingresado.
    Ejemplo de retorno: {'Recomendaciones para el usuario 76561197970982479': ['1. RWBY: Grimm Eclipse', '2. Rogue Legacy', '3. Dust: An Elysian Tail', "4. King Arthur's Gold", '5. RIFT']}
    """
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

