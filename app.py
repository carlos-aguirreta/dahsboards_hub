import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import pandas as pd
import numpy as np

# 1. GENERACIÓN DE DATOS MASIVOS (100 filas)
n_filas = 100
dias_semana = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
lista_frutas = ['Apple', 'Pear', 'Grape', 'Orange', 'Mango', 'Pineapple']

datos = {
    'dia': [dias_semana[i % 7] for i in range(n_filas)], # Repite los días cíclicamente
    'fruta': np.random.choice(lista_frutas, n_filas),    # Elige frutas al azar
    'cantidad': np.random.randint(5, 50, n_filas),       # Cantidades aleatorias entre 5 y 50
    'vendedor': np.random.choice(['Ana', 'Pedro', 'Luis'], n_filas) # Una columna extra por si acaso
}

df = pd.DataFrame(datos)

# 2. ORDENAR CRONOLÓGICAMENTE (Para que la gráfica no sea un caos)
df['dia'] = pd.Categorical(df['dia'], categories=dias_semana, ordered=True)
# Agrupamos para que si hay varios registros del mismo día/fruta, se sumen
df = df.groupby(['dia', 'fruta'], as_index=False, observed=False)['cantidad'].sum()

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
    html.H1("FRUIT SALES ANALYTICS HUB", style={'textAlign': 'center', 'fontFamily': 'Arial'}),
    
    html.Div([
        html.Label("Select Fruits to Compare:"),
        dcc.Dropdown(
            id='filtro-fruta',
            options=[{'label': i, 'value': i} for i in df['fruta'].unique()],
            value=['Apple', 'Pear'], # Iniciamos con dos para que se vea la comparativa
            multi=True,
            clearable=False
        ),
    ], style={'padding': '20px', 'width': '50%'}),

    # Contenedor para las gráficas
    html.Div([
        dcc.Graph(id='grafico-lineas'),
        dcc.Graph(id='grafico-barras')
    ])
])

# Esta es la "magia" que conecta el Dropdown con el Gráfico
@app.callback(
    [Output('grafico-lineas', 'figure'),
     Output('grafico-barras', 'figure')],
    Input('filtro-fruta', 'value')
)
def actualizar_dashboard(lista_frutas):
    # 1. Filtramos el dataframe usando .isin() 
    df_filtrado = df[df['fruta'].isin(lista_frutas)]
    
    # --- GRÁFICA DE LÍNEAS ---
    data_lineas = []
    for f in lista_frutas:
        current = df_filtrado.query('fruta == @f')
        data_lineas += [
            go.Scatter(
                x=current['dia'], 
                y=current['cantidad'], 
                mode='lines+markers', 
                name=f
            )
        ]
    
    fig_lineas = {
        'data': data_lineas,
        'layout': go.Layout(title="<b>Daily Sales Trend</b>", xaxis={'title': 'Day'}, yaxis={'title': 'Quantity'})
    }

    # --- GRÁFICA DE BARRAS (Con colores consistentes) ---
    # Sumamos el total vendido por cada fruta seleccionada
    df_totales = df_filtrado.groupby('fruta', as_index=False, observed=False)['cantidad'].sum()
    
    data_barras = []
    for f in lista_frutas:
        # Filtramos el total solo para la fruta de esta vuelta
        fruta_data = df_totales[df_totales['fruta'] == f]
        
        data_barras += [
            go.Bar(
                x=fruta_data['fruta'], 
                y=fruta_data['cantidad'], 
                name=f,
                showlegend=False # La leyenda ya aparece en el gráfico de líneas
            )
        ]
    
    fig_barras = {
        'data': data_barras,
        'layout': go.Layout(
            title="<b>Total Sales Volume per Fruit</b>",
            xaxis={'title': 'Fruit'},
            yaxis={'title': 'Total Quantity'}
        )
    }

    return fig_lineas, fig_barras

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 8050))
    app.run(host='0.0.0.0', port=port)
