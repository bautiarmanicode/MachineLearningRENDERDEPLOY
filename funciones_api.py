'''
FUNCIONES A UTILIZAR EN app.py
'''
# Importaciones
import pandas as pd
import gc

'''
________________________________________________________________
Asignamos el parquet a distintos df con los que vamos a trabajar
'''
#1 developer
df_developer = pd.read_parquet("./0 Dataset/2.2.1_API_developer.parquet")
#2 userdata
df_users_data = pd.read_parquet("./0 Dataset/2.2.2_API_user_data.parquet")
#3

#4

#5

#6

#7

'''
________________________________________________________________
'''


def intro():
    '''
    Genera una página de presentación HTML para la API Steam de consultas de videojuegos.    
    Returns:
    str: Código HTML que muestra la página de presentación.
    '''
    return '''
    <html>
        <head>
            <title>API Steam</title>
            <style>
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background-color: #f5f5f5;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    height: 100vh;
                }
                h1 {
                    color: #333;
                    text-align: center;
                    margin-bottom: 20px;
                }
                p {
                    color: #666;
                    text-align: center;
                    font-size: 18px;
                    margin-top: 10px;
                }
                span.highlight {
                    background-color: #3498db;
                    color: #fff;
                    padding: 5px;
                    border-radius: 3px;
                }
            </style>
        </head>
        <body>
            <h1>API de consultas de videojuegos de la plataforma Steam</h1>
            <p>Bienvenido a la API de Steam, donde puedes realizar diferentes consultas sobre la plataforma de videojuegos.</p>
            <p><span class="highlight">INSTRUCCIONES:</span> Escribe <span class="highlight">/docs</span> después de la URL actual de esta página para interactuar con la API.</p>
        </body>
    </html>
    '''

def developer(desarrollador: str):
    # Filtramos el DataFrame por el desarrollador
    result = df_developer[df_developer['Desarrollador'] == desarrollador]

    # Seleccionamos solo las columnas necesarias
    result = result[['Año', 'Cantidad de Items', 'Contenido Free']]

    # Convertimos el resultado a una lista de diccionarios
    return result.to_dict(orient='records')
# ________________________________________________________

def userdata(user_id: str):
    # Filtramos el DataFrame por el user_id
    result = df_users_data[df_users_data['user_id'] == user_id]
    
    # Si hay resultados, devolvemos el diccionario con el formato requerido
    if not result.empty:
        user_data = result.to_dict(orient='records')[0]
        return {
            "Usuario": user_data['user_id'],
            "Dinero gastado": f"{user_data['total_spent']} USD",
            "% de recomendación": f"{user_data['recommendation_percentage']}%",
            "cantidad de items": user_data['cantidad_items']
        }
    # Si no hay resultados, devolvemos un mensaje de error
    else:
        return {"error": f"No se encontraron datos para el usuario {user_id}"}
    