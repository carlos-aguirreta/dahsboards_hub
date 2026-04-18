#!/usr/bin/python
# -*- coding: utf-8 -*-

import dash
from dash import dcc, html
import plotly.graph_objs as go

# Data base - Un diccionario con 'x' y 'y'
data = {
  'x':['Enero', 'Febrero', 'Marzo'],
  'y':[10, 20, 15]
}

# Figura simple - Diccionario con data y layout
figura_simple = {
    'data': [go.Scatter(data)],
    'layout': go.Layout(title='Ventas Trimestrales')
}

# Declarar la app -
app = dash.Dash(__name__, # Nombre asignado por convención
        title='Dashboard básico', # Feature opcional
        update_title='Espera un poco...', # Feature opcional
        external_stylesheets= ['https://codepen.io/chriddyp/pen/bWLwgP.css'] # Feature opcional
    )

# Diseñar el layout
app.layout = html.Div(
    children=[
        html.H1(children='Dashboard básico'),
        dcc.Graph(
            id='Sample',
            figure=figura_simple
        ),
    ]
)

# lógica del dashboard, no cambies las líneas a continuación
if __name__ == '__main__':
    app.run(debug=True)