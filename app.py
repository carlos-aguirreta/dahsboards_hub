import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd
import numpy as np

# 1. GENERACIÓN DE DATOS MASIVOS (100 filas)
# --- DATASET (El que ya teníamos) ---
dias_semana = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
frutas = ['Apple', 'Pear', 'Grape', 'Mango', 'Orange', 'Pineapple']
datos = {
    'dia': [dias_semana[i % 7] for i in range(100)],
    'fruta': np.random.choice(frutas, 100),
    'cantidad': np.random.randint(10, 100, 100)
}
df = pd.DataFrame(datos)
df['dia'] = pd.Categorical(df['dia'], categories=dias_semana, ordered=True)
df = df.groupby(['dia', 'fruta'], as_index=False, observed=False)['cantidad'].sum()

# --- APP SETUP ---
# Usamos un tema "LUX" o "FLATLY" para que se vea elegante
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
server = app.server

# --- LAYOUT PROFESIONAL ---
app.layout = dbc.Container([
    # Encabezado
    dbc.Row([
        dbc.Col(html.H1("Fruit Sales Analytics Hub", className="text-center my-4 fw-bold"), width=12)
    ]),

    # Fila de KPIs (Tarjetas de resumen)
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Total Units Sold", className="card-title text-muted"),
                html.H2(id="kpi-total", className="text-primary")
            ])
        ], className="text-center shadow-sm"), width=4),
        
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Best Selling Fruit", className="card-title text-muted"),
                html.H2(id="kpi-best", className="text-success")
            ])
        ], className="text-center shadow-sm"), width=4),

        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Top Sales Day", className="card-title text-muted"),
                html.H2(id="kpi-day", className="text-warning")
            ])
        ], className="text-center shadow-sm"), width=4),
    ], className="mb-4"),

    # Filtros
    dbc.Row([
        dbc.Col([
            html.Label("Filter by Fruit:"),
            dcc.Dropdown(
                id='filtro-fruta',
                options=[{'label': i, 'value': i} for i in frutas],
                value=frutas[:3],
                multi=True,
                className="mb-4"
            ),
        ], width=12)
    ]),

    # Gráficas en paralelo (Grid System)
    dbc.Row([
        dbc.Col(dcc.Graph(id='grafico-lineas'), lg=7, md=12),
        dbc.Col(dcc.Graph(id='grafico-barras'), lg=5, md=12),
    ])
], fluid=True)

# --- CALLBACK ---
@app.callback(
    [Output('grafico-lineas', 'figure'),
     Output('grafico-barras', 'figure'),
     Output('kpi-total', 'children'),
     Output('kpi-best', 'children'),
     Output('kpi-day', 'children')],
    Input('filtro-fruta', 'value')
)
def update_dashboard(selected_fruits):
    filtered_df = df[df['fruta'].isin(selected_fruits)]
    
    # Cálculos para KPIs
    total_sales = f"{filtered_df['cantidad'].sum():,}"
    best_fruit = filtered_df.groupby('fruta', observed=False)['cantidad'].sum().idxmax()
    best_day = filtered_df.groupby('dia', observed=False)['cantidad'].sum().idxmax()

    # Gráfica de Líneas
    fig_lineas = go.Figure()
    for f in selected_fruits:
        curr = filtered_df[filtered_df['fruta'] == f]
        fig_lineas.add_trace(go.Scatter(x=curr['dia'], y=curr['cantidad'], name=f, mode='lines+markers'))
    fig_lineas.update_layout(title="<b>Daily Performance Trend</b>", template="plotly_white")

    # Gráfica de Barras
    totals = filtered_df.groupby('fruta', as_index=False, observed=False)['cantidad'].sum()
    fig_barras = go.Figure()
    for f in selected_fruits:
        f_total = totals[totals['fruta'] == f]
        fig_barras.add_trace(go.Bar(x=f_total['fruta'], y=f_total['cantidad'], name=f, showlegend=False))
    fig_barras.update_layout(title="<b>Total Volume per Category</b>", template="plotly_white")

    return fig_lineas, fig_barras, total_sales, best_fruit, best_day

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 8050))
    app.run(host='0.0.0.0', port=port)
