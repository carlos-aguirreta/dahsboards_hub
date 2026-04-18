import dash
from dash import dcc  # dcc ahora vive dentro de dash
from dash import html # html ahora vive dentro de dash
import plotly.graph_objs as go
import pandas as pd

# 1. DATOS SENCILLOS (En lugar de SQL, usamos un diccionario)
datos = {
    'dia': ['Lunes', 'Martes', 'Miercoles', 'Lunes', 'Martes', 'Miercoles'],
    'fruta': ['Manzana', 'Manzana', 'Manzana', 'Pera', 'Pera', 'Pera'],
    'cantidad': [10, 15, 7, 5, 8, 12]
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

app.layout = html.Div([
    html.H1("Mi Primer Dashboard de Ventas"),
    dcc.Graph(
        id='grafico-frutas',
        figure={
            'data': data_grafico,
            'layout': go.Layout(title='Ventas Diarias')
        }
    )
])

if __name__ == '__main__':
    app.run(debug=True)