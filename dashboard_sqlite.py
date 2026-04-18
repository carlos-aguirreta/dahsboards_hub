#!/usr/bin/python
# -*- coding: utf-8 -*-

import dash
from dash import dcc, html
from sqlalchemy import create_engine
import plotly.graph_objs as go
import pandas as pd

# Crear la conexion al archivo de base de datos
engine = create_engine('sqlite:///database/datos_ventas.db')

# Leer datos desde la base de datos
df = pd.read_sql("SELECT * FROM ventas_frutas", engine)

# Figura simple - Diccionario con data y layout
figura = {
    'data': [go.Bar(
        x=df['fruta'],
        y=df['cantidad'],
        marker_color='orange'
    )],
    'layout': go.Layout(title='Ventas de Frutas')
}

# Configurar la app
app = dash.Dash(__name__, # Nombre asignado por convención
        title='Dashboard con SQLite', # Feature opcional
        update_title='Espera un poco...', # Feature opcional
        external_stylesheets= ['https://codepen.io/chriddyp/pen/bWLwgP.css'] # Feature opcional
    )

# Diseño del Layout del Dashboard
app.layout = html.Div([
        html.H1('Reporte General de Ventas (SQLite)'),
        html.P('Este dashboard muestra las ventas de frutas almacenadas en una base de datos SQLite.'),
        dcc.Graph(
            id='grafico-frutas',
            figure=figura
        ),
    ]
)

# lógica del dashboard, no cambies las líneas a continuación
if __name__ == '__main__':
    app.run(debug=True)