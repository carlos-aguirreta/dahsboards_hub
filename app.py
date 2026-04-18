import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import pandas as pd

# 1. DATOS SENCILLOS (En lugar de SQL, usamos un diccionario)
datos = {
    'dia': ['Lunes', 'Martes', 'Miercoles', 'Lunes', 'Martes', 'Miercoles', 'Lunes', 'Martes', 'Miercoles'],
    'fruta': ['Manzana', 'Manzana', 'Manzana', 'Pera', 'Pera', 'Pera', 'Uva', 'Uva', 'Uva'],
    'cantidad': [10, 5, 9, 5, 8, 15, 3, 6, 8]
}
df = pd.DataFrame(datos)

# 2. PREPARAR LOS DATOS (El Pipeline)
data_grafico = []

# Queremos una linea para cada fruta... ¿como lo hacemos automatico?
for tipo_fruta in df['fruta'].unique():
    # Filtramos los datos para la fruta de esta vuelta del bucle
    current = df.query('fruta == @tipo_fruta')
    
    # Agregamos el objeto a nuestra lista
    data_grafico += [
        go.Scatter(
            x=current['dia'],
            y=current['cantidad'],
            mode='lines+markers', # Lineas con puntos para que se vea claro
            name=tipo_fruta
        )
    ]

# 3. EL DASHBOARD (Layout simplificado)
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("Dashboard interactivo de Ventas de Frutas"),
    # SELECTOR
    dcc.Dropdown(
        id='filtro-fruta',
        options=[{'label': i, 'value': i} for i in df['fruta'].unique()],
        value=['Manzana'], # Valor inicial
        multi=True,
        clearable=False
    ),
    
    # GRAFICO
    dcc.Graph(id='grafico-frutas') # Quitamos la 'figure' de aquí, porque la dará el Callback
])

# Esta es la "magia" que conecta el Dropdown con el Gráfico
@app.callback(
    Output('grafico-frutas', 'figure'),
    Input('filtro-fruta', 'value')
)
def actualizar_grafico(lista_frutas):
    # 1. Filtramos el dataframe usando .isin() 
    # Esto busca filas donde la fruta esté EN la lista seleccionada
    df_filtrado = df[df['fruta'].isin(lista_frutas)]
    
    # 2. Creamos los trazos (traces) usando un bucle
    data_grafico = []
    for f in lista_frutas:
        current = df_filtrado.query('fruta == @f')
        data_grafico += [
            go.Scatter(
                x=current['dia'], 
                y=current['cantidad'], 
                mode='lines+markers', 
                name=f
            )
        ]
    
    return {
        'data': data_grafico,
        'layout': go.Layout(title="Comparativa de Ventas")
    }

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 8050))
    app.run(host='0.0.0.0', port=port)
