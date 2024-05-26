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
#Carga de dataset
df_developer = pd.read_parquet("./0 Dataset/2.2.1_API_developer.parquet")
df_rev_games = pd.read_parquet("./0 Dataset/4_API_ML_ITEM.parquet")
df_steam_games = pd.read_parquet("./0 Dataset/1.1_steam_games_LISTO.parquet")
df_user_reviews = pd.read_parquet("./0 Dataset/1.3_user_review_sentiment.parquet")



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
    resultado_final = result.to_dict(orient='records')
     
    # Liberamos la memoria utilizada por el DataFrame intermedio
    del result
    gc.collect()
    # Convertimos el resultado a una lista de diccionarios
    return resultado_final
# ________________________________________________________

def userdata(user_id: str):
    """
    Devuelve la cantidad de dinero gastado por el usuario ingresado, el porcentaje de recomendación sobre las reviews realizadas y la cantidad de items.
    Ejemplo de retorno: {"Usuario X": us213ndjss09sdf, "Dinero gastado": 200 USD, "% de recomendación": 20%, "cantidad de items": 5}
    """
    # Si el user_id no se encuentra en los dataframes:
    if user_id not in df_user_reviews['user_id'].values:
        return f"ERROR: El user_id {user_id} no existe en la base de datos."  # se imprime mensaje de error
    else:
        # Se filtran los datos en función al usuario especificado
        df_filtrado = df_user_reviews[df_user_reviews['user_id'] == user_id]
        
        # Se unen las columnas necesarias de los dataframes:
        df_merged = pd.merge(df_filtrado[['user_id', 'reviews_item_id', 'reviews_recommend']], 
                              df_steam_games[['id', 'price']], 
                              left_on='reviews_item_id', right_on='id', how='inner')
        
        # Se calcula la cantidad de dinero gastado por el usuario
        dinero_gastado = round(df_merged['price'].sum(), 2)
        
        # Se calcula la cantidad de recomendaciones del usuario
        recomendaciones = df_merged['reviews_recommend'].sum()
        
        # Se calcula el total de reviews del usuario
        total_reviews = df_merged.shape[0]
        
        # Se calcula el porcentaje de recomendaciones sobre el total de reviews
        porcentaje_recomendacion = round(recomendaciones / total_reviews * 100, 0)
        
        # Se calcula la cantidad de items por usuario
        cantidad_de_items = df_merged['reviews_item_id'].nunique()
        
        # Crear un diccionario con los resultados
        dicc_rdos = {
            "Usuario": user_id,
            "Dinero gastado": f'{dinero_gastado} USD',
            "% de recomendación": f'{porcentaje_recomendacion}%',
            'Cantidad de items': cantidad_de_items
        }
        # Liberamos la memoria utilizada por el DataFrame intermedio
        del df_filtrado, df_merged
        gc.collect()
        
        return dicc_rdos


# ____________________________________________________________________________________
def recomendacion_juego(user_id: str):
    '''
    Devuelve una lista con 5 sugerencias de juegos para el usuario seleccionado.
    Ejemplo de retorno: {'Sugerencias para el usuario 76561197970982479': ['1. RWBY: Grimm Eclipse', '2. Rogue Legacy', '3. Dust: An Elysian Tail', "4. King Arthur's Gold", '5. RIFT']}
    '''
    # Si el ID de usuario no se encuentra en los dataframes:
    if user_id not in df_user_reviews['user_id'].values:
        return f"ERROR: El ID de usuario {user_id} no existe en la base de datos."  # se imprime un mensaje de error
    else:
        # Se asigna el ID ingresado a la variable user
        user = user_id

        # En primer lugar, se extraen los juegos que el usuario ya ha jugado:
        df_rev_games = pd.merge(df_user_reviews, df_steam_games, left_on="reviews_item_id", right_on="id", how="inner")
        juegos_jugados = df_rev_games[df_rev_games['user_id'] == user]

        # Se eliminan del dataframe de juegos los jugados por el usuario
        df_user = df_steam_games[["id", "app_name"]].drop(juegos_jugados.id, errors='ignore')

        # Ruta completa al archivo RS_model.pkl
        ruta_modelo = './0 Dataset/RS_model.pkl'

        # Se carga el modelo de Sistema de Recomendación entrenado desde el archivo especificado
        with open(ruta_modelo, 'rb') as file:
            RS_model = pickle.load(file)

        # Se realizan las predicciones y se agregan en una nueva columna:
        df_user['estimate_Score'] = df_user['id'].apply(lambda x: RS_model.predict(user, x).est)

        # Se ordena el dataframe de manera descendente en función al score y se seleccionan los 5 principales:
        sugerencias = df_user.sort_values('estimate_Score', ascending=False)["app_name"].head(5).to_list()

        # Se crea la llave del diccionario de retorno
        llave_dic = f'Sugerencias para el usuario {user}'

        # Se da formato a las 5 sugerencias:
        sugerencias_formateadas = [f'{i+1}. {sugerencia}' for i, sugerencia in enumerate(sugerencias)]
        # Se libera la memoria utilizada por los dataframes intermedios
        del df_rev_games, juegos_jugados, df_user
        gc.collect()
        
        # Se devuelven los resultados en un diccionario
        return {llave_dic: sugerencias_formateadas}





# def recomendacion_juego(id_producto):
    # Lógica para recomendar juegos similares al juego con id_producto
    # Devolver una lista con 5 juegos recomendados
    
    
# def recomendacion_usuario(id_usuario):
    # Lógica para recomendar juegos a un usuario específico
    # Devolver una lista con 5 juegos recomendados para el usuario id_usuario





