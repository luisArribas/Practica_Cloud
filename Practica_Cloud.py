# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 19:43:47 2022

@author: luisr
"""

import dash
from dash import dcc
from dash import html
import datetime
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import requests
import numpy as np
import sys
sys.path.append("C:/Users/luisr/OneDrive/Desktop/MIAX/Practicas/3_Cloud")
import aux_scrap
import mibian as mb
import plotly.express as px

##  Inicializamos dash
app = dash.Dash(__name__)

##  Definimos patron de colores
colors = {
    'background': '#C5C1AA',
    'text': '#7FDBFF'
}

##  Hacemos scrapping de los datos antes de generar el dash
data,valor_fut = aux_scrap.scrapping()

##  Extraemos las fechas para el dropdown
fechas = []
for key in list(data.keys()):
    if key[1] not in fechas:
        fechas.append(key[1])

# Generamos el layout
app.layout = html.Div(children =[
    html.H1(['Práctica Tecnologías Cloud - MIAX9'], style={'padding': 10, 
                                                           'flex': 1}),
    html.Div([
        html.Div(["Autor: Luis Arribas Viosca"]),
        html.Br(),
    ], style={'padding': 10, 'flex': 1}),
    html.Div([
        html.Div(["Seleccione Fecha:"]),
        html.Br(),
        html.Div([dcc.Dropdown(fechas, fechas[0], id='calendario')], 
                 style={"width": "10%"}),
        html.Br(),
        html.Div(["Seleccione Tipo de Producto:"]),
        html.Br(),
        html.Div([dcc.Dropdown(['Call','Put'], 'C', id='tipo_opcion')], 
                 style={"width": "10%"}),
        html.Br(),
        html.Div([
            dcc.Graph(
                id='grafico')
        ]),
    ], style={'padding': 10, 'flex': 1}),   
 ], style={'backgroundColor': colors['background']})

##   Utilizamos un callback para que el dash interactúte con la fecha 
##   y el tipo de opcion seleccionados por el usuario

@app.callback(
    Output('grafico', 'figure'),
    Input('calendario', 'value'),
    Input('tipo_opcion', 'value'))
def plot_smile(date,tipo_opcion):

    if tipo_opcion == 'Call':
        opt = 'C'
    else:
        opt = 'P'
    
    ##  Construimos la key con fecha y tipo de opcion seleccionados
    key = tuple([opt,date])
    
    ##  Scrappeamos para obtener el diccionario con los datos
    data,valor_fut = aux_scrap.scrapping()

    ##  obtenemos los datos de esa key
    datos_smile = data.get(key)
    
    ##  Tratamos los datos para que sean float
    datos_smile.Strikes = datos_smile.Strikes.str.replace('.','')
    datos_smile.Vals = datos_smile.Vals.str.replace('.','')
    datos_smile = datos_smile.replace(',','.',regex = True)
    datos_smile = datos_smile.astype(float)
    
    ##  Incorporamos el precio del futuro
    valor_fut = valor_fut.replace('.','')
    valor_fut = valor_fut.replace(',','.')
    valor_fut = float(valor_fut)
    
    ##  Calculamos el numero de dias
    today = datetime.datetime.today()
    date2 = datetime.datetime.strptime(date, '%Y%m%d')
    
    n_days = date2 - today
    n_days = n_days.days
    
    ##  En un bucle for vamos recorriendo los distintos strikes y almacenando
    ##  la volatilidad implicita calculada
    impVol_vec = []
    for i in range(1,len(datos_smile) + 1):
        print(i)
        strike = datos_smile['Strikes'][i-1]
        precio = datos_smile['Vals'][i-1]
        
        ##  Para cada strike debemos sacar la volatilidad implicita
        bs = mb.BS([valor_fut, strike, 0, n_days], callPrice = precio)
        impVol = bs.impliedVolatility
        impVol_vec.append(impVol)
    
    ##  Creamos dataframe para el plot    
    x = datos_smile['Strikes']
    y = pd.Series(impVol_vec)
    
    datos_fin = { 'Strikes': x, 'Vol': y }
    datos_fin = pd.DataFrame(datos_fin)
    
    ##  Plot
    fig = px.scatter(
        datos_fin,
        x = "Strikes",
        y = "Vol",
        template='plotly_dark'
    )
    fig.data[0].update(mode='markers+lines')
    
    return fig


if __name__ == ("__main__"):
    app.run_server(port=8080)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
 