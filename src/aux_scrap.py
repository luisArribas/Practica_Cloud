# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 08:08:11 2022

@author: luisr
"""

##  Llamamos a las librerias para hacer el web scrapping:
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pandas as pd


def scrapping():
    ##  Cargamos la pagina web que queremos scrappear:
    headers = {'User-Agent': 'Firefox'}
    url = 'https://www.meff.es/esp/Derivados-Financieros/Ficha/FIEM_MiniIbex_35'  
    
    ##  Descargamos la pagina web con un request
    re = requests.get(url,headers=headers)
    print(re.status_code)  
    
    ##  Parseamos el contenido de la web
    soup = BeautifulSoup(re.text, 'lxml') 
    
    ##  Vamos a scrapear primero los datos que necesitamos de la tabla de futuros
    tabla_fut = soup.find_all('table',{'class' : 'Precios'})[0]
    
    ##  De esta tabla cogemos la primera fila
    first_row = tabla_fut.find_all('tr',{'class' : 'text-right'})[0]
    
    ##  Cogemos fecha y valor:
    fecha_fut = first_row.find_all('td',{'class' : 'text-center colVcto'})[0]
    fecha_fut = fecha_fut.text
    
    value_fut = first_row.find_all('td')[13]
    value_fut = value_fut.text
    
    # ##  Pasamos ahora a scrappear las tablas de precios call y put
    tabla_opt = soup.find_all('table',{'class' : 'Precios'})[1]
    
    ##  Tenemos todos los datos pero no podemos distinguir por fecha ni si son
    ##  calls o puts. Para ello, sacamos primero la info de las fechas
    
    fechas =[]
    for dates in tabla_opt.find_all('option'):
        
        try:
            date = dates.string
            date_format = datetime.strptime(date, '%d/%m/%Y')
            y = date_format.strftime("%Y")
            m = date_format.strftime("%m")
            d = date_format.strftime("%d")
            fecha_new = str(y+m+d)
            
            fechas.append(fecha_new)
        except:
            continue
    ##  Sacamos la lista de fechas unicas    
    fechas = list(set(fechas))   
    
    ##  Para cada fecha sacamos los datos de call y put
    data_dict = {}
    for fecha in fechas:
        
        ## Call
        data_tipo = 'OCE' + fecha
        rows = tabla_opt.find_all('tr',{'data-tipo' : data_tipo})
        strikes = []
        values = []
        
        for row in rows:
            strike = row.find_all('td')[0].text
            value =  row.find_all('td')[12].text
            strikes.append(strike)
            values.append(value)
        
        ##  Creamos dataframe con strikes y valores
        data = pd.DataFrame(list(zip(strikes,values)),
                            columns = ['Strikes','Vals'])
        
        ##  Guardamos en un diccionario
        key = ('C',fecha)
        data_dict[key] = data 
        
        ## Put
        data_tipo = 'OPE' + fecha
        rows = tabla_opt.find_all('tr',{'data-tipo' : data_tipo})
        strikes = []
        values = []
        
        for row in rows:
            strike = row.find_all('td')[0].text
            value =  row.find_all('td')[7].text
            strikes.append(strike)
            values.append(value)
        
        ##  Creamos dataframe con strikes y valores
        data = pd.DataFrame(list(zip(strikes,values)),
                            columns = ['Strikes','Vals'])
        
        ##  Guardamos en un diccionario
        key = ('P',fecha)
        data_dict[key] = data
        
    return data_dict,value_fut
 
    
        
    











































