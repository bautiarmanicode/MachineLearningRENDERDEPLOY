'''
FUNCIONES A UTILIZAR EN app.py
'''
# Importaciones
import pandas as pd
import gc
import pickle

'''
________________________________________________________________
Asignamos el parquet a distintos df con los que vamos a trabajar
'''
#1 developer
df_developer = pd.read_parquet("./0 Dataset/2.2.1_API_developer.parquet")
#2 userdata
df_users_data = pd.read_parquet("./0 Dataset/2.2.2_API_user_data.parquet")
#3 ML ITEM X ITEM
df_rev_games = pd.read_parquet("./0 Dataset/4_API_ML_ITEM.parquet")
df_steam_games = pd.read_parquet("./0 Dataset/1.1_steam_games_LISTO.parquet")
df_users_reviews = pd.read_parquet("./0 Dataset/1.3_user_review_sentiment.parquet")
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
        user_data = result.to_dict(orient='records')[0]  # Acceder al primer elemento de la lista
        return {
            "Usuario": user_data['user_id'],  # Acceder a la clave 'user_id' del diccionario
            "Dinero gastado": f"{user_data['total_spent']} USD",
            "% de recomendación": f"{user_data['recommendation_percentage']}%",
            "cantidad de items": user_data['cantidad_items']
        }
    # Si no hay resultados, devolvemos un mensaje de error
    else:
        return {"error": f"No se encontraron datos para el usuario {user_id}"}

# ____________________________________________________________________________________
def recomendacion_juego(user_id):
    '''
    Devuelve una lista con 5 recomendaciones de juegos para el usuario ingresado.
  
    Ejemplo de retorno: {'Recomendaciones para el usuario 76561197970982479': ['1. RWBY: Grimm Eclipse',
      '2. Rogue Legacy',
      '3. Dust: An Elysian Tail',
      "4. King Arthur's Gold",
      '5. RIFT']} 
    '''
    # Verificar si el user_id se encuentra en los dataframes
    if user_id not in df_users_reviews['user_id'].values:
        return f"ERROR: El user_id {user_id} no existe en la base de datos."
    
    # En primer lugar, sacar los juegos que el usuario ya ha jugado:
    games_played = df_rev_games[df_rev_games['user_id'] == user_id]

    # Eliminar del df de juegos los jugados por el usuario
    df_unplayed_games = df_steam_games[~df_steam_games['item_id'].isin(games_played['item_id'])].copy()

    # Especifica la ruta completa al archivo RS_model.pkl
    ruta_modelo = './0 Dataset/RS_model.pkl'

    # Cargar el modelo de Sistema de Recomendación entrenado desde el archivo especificado
    with open(ruta_modelo, 'rb') as file:
        RS_model = pickle.load(file)
    # Realizar las predicciones y agregarlas en una nueva columna:
    df_unplayed_games['estimate_Score'] = df_unplayed_games['item_id'].apply(lambda x: RS_model.predict(user_id, x).est)

    # Ordenar el df de manera descendente en función al score y seleccionar los 5 principales:
    recommendations = df_unplayed_games.sort_values('estimate_Score', ascending=False)["app_name"].head(5).to_list()

    # Crear la llave del diccionario de retorno
    llave_dic = f'Recomendaciones para el usuario {user_id}'

    # Dar formato al top 5 de recomendaciones:
    recomm_output = [f'{i+1}. {recommendations[i]}' for i in range(len(recommendations))]

    # Devolver los resultados en un diccionario
    return {llave_dic: recomm_output}




# def recomendacion_juego(id_producto):
    # Lógica para recomendar juegos similares al juego con id_producto
    # Devolver una lista con 5 juegos recomendados
    
    
# def recomendacion_usuario(id_usuario):
    # Lógica para recomendar juegos a un usuario específico
    # Devolver una lista con 5 juegos recomendados para el usuario id_usuario





