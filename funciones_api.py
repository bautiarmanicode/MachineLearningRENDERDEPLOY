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
#developer viejo
#df_API_developer = pd.read_parquet("./0 Dataset/2.2_df_API_developer.parquet")

#1 developer nuevo
df_API_developer2 = pd.read_parquet("./0 Dataset/2.2.1_API_developer.parquet")

#userdata
df_user_reviews = pd.read_parquet("./0 Dataset/1.2_user_review_LISTO.parquet")                    
df_steam_games = pd.read_parquet("./0 Dataset/1.1_steam_games_LISTO.parquet")     

'''
________________________________________________________________
'''
#UserForGenre
#df_UserForGenre = pd.read_parquet("./0 Dataset/F_df_funciones.parquet")                    
# best_developer_year
#df_best_developer_year = pd.read_parquet("./0 Dataset/F_df_funciones.parquet")                    
#developer_reviews_analysis
#funcion5 = pd.read_parquet("./0 Dataset/F_df_funciones.parquet")                    

# ________________________________________________________
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
    result = df_API_developer2[df_API_developer2['Desarrollador'] == desarrollador]
    return result.to_dict(orient='records')

# ________________________________________________________

'''
def developer(desarrollador: str):
    df_dev = df_API_developer[df_API_developer['developer'] == desarrollador]

    grouped = df_dev.groupby('release_year').agg(
        items=('user_id', 'count'),  # Cambiar de (x == 0).sum() a 'count' o 'sum'
        gratis=('price', lambda x: (x == 0).sum())
    )

    result = []
    for year, row in grouped.iterrows():
        juegos = int(row["items"])
        gratis_percent = round(row["gratis"] / juegos * 100, 2) if juegos > 0 else 0
        result.append({
            "Año": int(year),
            "Juegos": juegos,
            "Gratis %": gratis_percent
        })
    
    # Llamamos al recolector de basura
    gc.collect()

    return result

'''

# ________________________________________________________
# 
def userdata(user_id: str):
    # Filtrar las revisiones del usuario
    user_reviews = df_user_reviews[df_user_reviews['user_id'] == user_id]

    # Calcular el dinero gastado por el usuario
    spent_money = 0
    for item_id in user_reviews['reviews_item_id']:
        price = df_steam_games[df_steam_games['user_id'] == item_id]['price'].values
        if len(price) > 0:  # Verificar si se encontró el precio del ítem
            spent_money += price[0]

    # Calcular el porcentaje de recomendación
    total_reviews = len(user_reviews)
    num_recommendations = (df_user_reviews['sentiment_analysis'] == True).sum()
    recommendation_percentage = (num_recommendations / total_reviews) * 100 if total_reviews > 0 else 0

    # Crear el diccionario de salida
    result = {
        'Usuario': user_id,
        'Dinero gastado': f"{spent_money} USD",
        '% de recomendación': f"{recommendation_percentage}%",
        'cantidad de items': total_reviews
    }

    # Devolver el diccionario como parte de una lista
    return [result]










